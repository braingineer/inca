from setuptools import setup, find_packages

setup(
    name='inca',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', 'sqlitedict'
    ],
    entry_points='''
        [console_scripts]
        inca=inca.interface:handle
    ''',
)