from setuptools import setup, find_packages

setup(
    name="kalighost-pro",
    version="2.0.0",
    author="KaliGhost Team",
    author_email="info@kalighost.pro",
    description="Professional Cyberpunk 3D Pentesting Interface",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/elkalivpn/KaliGhost",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "License :: Other/Proprietary License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "PySide6>=6.5.0",
        "PyOpenGL>=3.1.6",
        "PyOpenGL-accelerate>=3.1.6",
        "numpy>=1.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.2.0",
            "pytest-qt>=4.2.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
            "black>=23.1.0",
        ],
        "docs": [
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "kalighost-pro=gui.pro_kalighost_main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "gui": ["assets/*", "themes/*", "config/*"],
    },
    zip_safe=False,
)