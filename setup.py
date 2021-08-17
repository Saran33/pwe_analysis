from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
	
setup(
    name='pwe',
    packages=find_packages(include=['pwe']),
    version='0.1.6',
	author='Saran Connolly',
    description='PWE Capital security analysis and charting package.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/Saran33/pwe_analysis",
    project_urls={
        "Bug Tracker": "https://github.com/Saran33/pwe_analysis/issues",
    },
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	install_requires = [
  'cufflinks @ git+https://github.com/Saran33/cufflynx.git@Saran33#egg=cufflinks','pandas','numpy','pandas_summary','plotly',
],
	package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)