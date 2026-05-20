
def scan_webserver(target: str) -> str:
    """Escanea un servidor web con nikto."""
    import subprocess
    result = subprocess.run(['nikto', '-h', target], capture_output=True, text=True)
    return result.stdout
                