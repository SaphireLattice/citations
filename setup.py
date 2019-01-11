from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='citations',
      version='0.1',
      description='"Papers Please" citation generator',
      author='Saphire Lattice',
      packages=['citations'],
      package_dir={'citations': 'citations'},
      package_data={'citations': ['data/*']},
      scripts=['bin/citate'],
      install_requires=requirements)
