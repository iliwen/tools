from setuptools import setup, find_packages
setup(
      name="tools",
      version="1.0",
      description="commen tools for daliy work",
      author="wen li",
      url="https://www.python.org/sigs/distutils-sig/",
      license="LGPL",
      packages= find_packages(),

      include_package_data = True,
      exclude_package_data = {'':['README.*']}

      )
