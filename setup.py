"""Setup script for Governance & Compliance Agent"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="governance-compliance-agent",
    version="1.0.0",
    author="Governance Team",
    author_email="governance-support@company.com",
    description="LLM-powered autonomous governance and compliance validation agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/company/governance-compliance-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
        "Topic :: Security",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ],
        "monitoring": [
            "prometheus-client>=0.19.0",
            "opentelemetry-api>=1.21.0",
            "opentelemetry-sdk>=1.21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "governance-agent=src.main:main",
        ],
    },
)