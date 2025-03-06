from setuptools import setup, find_packages

setup(
    name="readme-gen",
    version="1.0",
    packages=find_packages(),
    install_requires=["google-generativeai"],
    entry_points={
        "console_scripts": [
            "readme-gen = generator.generate_readme:main",
        ],
    },
)
