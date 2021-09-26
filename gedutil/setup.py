from setuptools import setup

# with open("README", 'r') as f:
# long_description = f.read()
long_description = "CS555 Project"

setup(
    name="gedutil",
    version="1.0",
    description="GEDCOM Parser",
    license="MIT",
    long_description=long_description,
    author="Team 11",
    author_email="rens@stevens.edu",
    url="http://stevens.edu/",
    packages=["gedutil"],  # same as name
    install_requires=[
        "wheel",
        "bar",
        "greek",
        "loguru",
    ],  # external packages as dependencies
    #    scripts=[
    #             'scripts/cool',
    #             'scripts/skype',
    #            ]
)
