from setuptools import find_packages, setup

setup(
    name='weatherstation',
    version='0.3.3',
	author='Peter Reimer',
    author_email='peter@4pi.org',
    packages=find_packages(),
	include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Framework :: Flask",
        "Programming Language :: Python :: 3.7"
    ],
    install_requires=[
        'flask',
        'numpy',
        'pandas',
        'bokeh'
    ],
)
