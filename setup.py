from setuptools import find_packages, setup
from typing import List


def get_requirements()->List[str]:

    requirement_list:List[str] = []

    #write code to read requirements.txt file and append each requirements_list variables.

    return requirement_list


setup(
    name="sensor",
    version = "0.0.1",
    author= " Proma",
    author_email="tanjinaproma@gmail.com",
    packages=find_packages(),
    install_requires= get_requirements(),          #["pymongo==4.2.0"],

)