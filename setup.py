"""Setup configuration for parenting-capacity-assessor package."""
from setuptools import setup, find_packages
from pathlib import Path

BASE_DIR = Path(__file__).parent
README = (BASE_DIR / "README.md").read_text(encoding="utf-8")

setup(
    name="parenting-capacity-assessor",
    version="0.1.0",
    description="Local, privacy-first AI agent for generating court-ready parenting capacity assessment reports",
    long_description=README,
    long_description_content_type="text/markdown",
    author="kalilynx",
    url="https://github.com/kalilynx/parenting-capacity-assessor",
    license="MIT",
    packages=find_packages(exclude=["tests", "docs"]),
    python_requires=">=3.10",
    install_requires=[
        "streamlit>=1.31.0",
        "langchain>=0.2.0",
        "langchain-community>=0.2.0",
        "langchain-chroma>=0.1.2",
        "chromadb>=0.5.0",
        "ollama>=0.2.0",
        "python-docx>=1.1.0",
        "pypdf>=4.0.0",
        "python-dotenv>=1.0.1",
        "sentence-transformers>=2.7.0",
        "python-multipart>=0.0.9",
        "docx2txt>=0.8.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pca=pca.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Healthcare/Medical",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Environment :: Console",
    ],
)
