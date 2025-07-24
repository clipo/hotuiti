"""
Setup configuration for Hotuiti - Moai Center of Mass Analysis
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hotuiti",
    version="1.0.0",
    author="Carl Lipo",
    author_email="",
    description="A scientific analysis project for calculating and visualizing the center of mass of Rapa Nui moai statues",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clipo/hotuiti",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "trimesh>=4.0.0",
        "numpy>=1.20.0",
        "matplotlib>=3.5.0",
        "scipy>=1.7.0",
        "rtree>=1.0.0",
        "shapely>=2.0.0",
        "networkx>=3.0",
        "pillow>=10.0.0",
    ],
    extras_require={
        "interactive": ["plotly>=5.0.0"],
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "moai-analyze=moai_analyzer_final:main",
            "moai-analyze-interactive=moai_analyzer_plotly:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.obj", "*.md", "*.txt"],
    },
)