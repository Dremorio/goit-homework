from setuptools import setup

setup(
      name='clean_folder',
      version='0.1.0',
      packages=['clean_folder'],
      author='Dremorio',
      description='Clean folder from trash',
      entry_points={
          'console_scripts': ['clean-folder = clean_folder.clean:main']
      }

)