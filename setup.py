from setuptools import find_packages, setup

setup(
    name='weatherstation',
    version='0.0.4',
	author='Peter Reimer',
    author_email='peter@4pi.org',
    packages=find_packages(),
	include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
