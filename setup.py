"""Setup file for metno-locationforecast package."""

import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="metno-locationforecast",
    version="2.0.0",
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
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
    python_requires=">=3.9",
    install_requires=["requests>=2.25.1", "tzdata>=2020.5"],
    extras_require={
        "dev": [
            "black==24.10.0",
            "check-manifest==0.50",
            "coverage==7.6.7",
            "flake8==7.1.1",
            "mypy==1.13.0",
            "pydocstyle==6.3.0",
            "pytest==8.3.3",
            "twine==5.1.1",
            "tzdata==2020.5",
        ]
    },
    project_urls={
        "Source": "https://github.com/Rory-Sullivan/metno-locationforecast",
        "Issues": "https://github.com/Rory-Sullivan/metno-locationforecast/issues",
    },
    zip_safe=False,
)
