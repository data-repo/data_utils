
# import re
import setuptools
# import configparser


def get_readme():
    """
    Get readme description
    """
    with open('README.md', 'r') as f:
        return f.read()


# def get_poetry_packages():
#     """
#     Get all packages and version from pyproject.toml file
#     """
#     packages = []
#     config = configparser.ConfigParser()
#     file_path = 'pyproject.toml'
#     config.read(file_path)
#     dependencies = dict(config['tool.poetry.dependencies'])
#     for package, version in dependencies.items():
#         if package != 'python':
#             version = re.search(r'(?:\d\.?)+', version).group()
#             packages.append(f'{package}>={version}')
#     return packages


long_description = get_readme()
# install_requires = get_poetry_packages()

setuptools.setup(
    name='data_tools',
    version='0.1.4',
    packages=['data_tools', 'data_tools.utils'],
    package_data={'': ['*/*', '*/*/*', '*/*/*/*']},
    author='mohammad mahdi azadjalal',
    author_email='data_tools.company@data.com',
    description='Base package for crawler',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://google.com',
    license='ISC',
    install_requires=['pyyaml>=6.0', 'kafka-python>=2.0.2', 'requests>=2.26.0']
)
