from setuptools import setup

setup(name="drafter",
      version="0.1",
      description="Smart draft management",
      url="http://github.com/swo/drafter",
      author="Scott Olesen",
      author_email="swo@alum.mit.edu",
      license="MIT",
      packages=["drafter"],
      scripts=["bin/drafter"],
      zip_safe=False)
