"""Setup file for metno-locationforecast package."""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="metno-locationforecast",
    version="1.2.0",
    description="A Python interface for MET Norway's Locationforecast 2.0 service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rory-Sullivan/metno-locationforecast",
    author="Rory Sullivan",
    author_email="codingrory@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=[
        "met",
        "metno",
        "norway",
        "yr",
        "locationforecast",
        "location",
        "forecast",
        "weather",
        "api",
        "python",
        "python3",
    ],
    packages=find_packages(include=["metno_locationforecast", "metno_locationforecast.*"]),
    package_data={"metno_locationforecast": ["py.typed"]},
    python_requires=">=3.6",
    install_requires=["requests>=2.20.0"],
    extras_require={
        "dev": [
            "black==24.3.0",
            "flake8==3.8.3",
            "mypy==0.782",
            "pydocstyle==5.0.2",
            "pytest==5.4.3",
            "coverage==5.2",
            "twine==5.1.1",
            "check-manifest==0.42",
        ]
    },
    project_urls={
        "Source": "https://github.com/Rory-Sullivan/metno-locationforecast",
        "Issues": "https://github.com/Rory-Sullivan/metno-locationforecast/issues",
    },
    zip_safe=False,
)
