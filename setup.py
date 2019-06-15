from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='gastorage',
      version='0.1',
      description='Genetic Algorithm - Storage Optimalization',
      url='http://github.com/stankarp0',
      author='stankarp0',
      author_email='stankarp0@gmail.com',
      packages=['gastorage'],
      install_requires=['numpy', 'deap', 'matplotlib'],
      zip_safe=False,
      tests_require=[],
      entry_points={
        'console_scripts': ['gastorage=gastorage.command_line:main'],
      },
)