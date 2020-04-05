from distutils.core import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="J4U-API",
    version="0.1dev",
    packages=["j4u_api", "tests"],
    install_requires=requirements,
    license="Creative Commons Attribution-Noncommercial-Share Alike license",
)
