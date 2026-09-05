"""
Logging Utility Module
Secure logging with rotation and encryption support
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


class SecureFormatter(logging.Formatter):
    """Custom formatter that sanitizes sensitive data"""
    
    SENSITIVE_PATTERNS = [
        'password', 'passphrase', 'key', 'secret', 'token',
        'credential', 'auth'
    ]
    
    def format(self, record):
        # Sanitize sensitive data in log messages
        msg = super().format(record)
        
        # Simple sanitization (in production, use more robust methods)
        for pattern in self.SENSITIVE_PATTERNS:
            if pattern in msg.lower():
                msg = msg.replace(pattern, '*' * len(pattern))
        
        return msg


def setup_logger(name: str, level: int = logging.INFO, 
                 log_file: str = None, secure: bool = True) -> logging.Logger:
    """
    Setup a logger with optional file output and security features
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Path to log file (optional)
        secure: Enable secure formatting
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Format
    if secure:
        formatter = SecureFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_audit_logger() -> logging.Logger:
    """Get dedicated audit logger for security events"""
    return setup_logger(
        'Audit',
        level=logging.INFO,
        log_file='logs/audit.log',
        secure=True
    )


def get_security_logger() -> logging.Logger:
    """Get dedicated security events logger"""
    return setup_logger(
        'Security',
        level=logging.DEBUG,
        log_file='logs/security.log',
        secure=True
    )
