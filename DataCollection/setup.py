from setuptools import setup, find_packages

with open("requirements.txt") as handle:
    project_requirements = [line.strip() for line in handle.readlines()]

setup(name="youtubecollector",
      version="0.1.0",
      description="Module for getting data from youtube",
      url="https://github.com/CorrespondentData/YouTubeExtremism",
      author="De Correspondent",
      packages=find_packages('youtubecollector'),
      install_requires=project_requirements,
      python_requires='>=3'
      )
