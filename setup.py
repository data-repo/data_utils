
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
    name='rad_data',
    version='0.1.4',
    packages=['rad_data', 'rad_data.utils'],
    package_data={'': ['*/*', '*/*/*', '*/*/*/*']},
    author='Data team group',
    author_email='rad.company@data.com',
    description='Base package for crawler in data team',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://scm.cepitadev.com',
    license='RAD',
    install_requires=['pyyaml>=6.0', 'kafka-python>=2.0.2', 'requests>=2.26.0']
)
