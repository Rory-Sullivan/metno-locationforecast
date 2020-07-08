from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="yrlocationforecast",
    version="0.0.1a1",
    description="A Python interface for the Yr Location Forecast service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rory-Sullivan/yrlocationforecast",
    author="Rory Sullivan",
    author_email="codingrory@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="yr, location, forecast, weather, api, python",
    packages=find_packages(where="yrlocationforecast"),
    python_requires=">=3.6, <4",
    install_requires=["requests~=2.0.0"],
    extras_require={"dev": ["black", "flake8"], "test": ["coverage"]},
    project_urls={
        "Source": "https://github.com/Rory-Sullivan/yrlocationforecast",
        "Issues": "https://github.com/Rory-Sullivan/yrlocationforecast/issues",
    },
)
