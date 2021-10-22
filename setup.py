from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
	
setup(
    name='pwe',
    packages=find_packages(include=['pwe']),
    version='0.1.618033988749894848204586834365638117720',
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
  'cufflinks @ git+https://github.com/Saran33/cufflynx.git@Saran33#egg=cufflinks',
  'alpha_vantage @ git+git://github.com/Saran33/alpha_vantage.git@develop#egg=alpha_vantage',
		'cryptocmd @ git+https://github.com/guptarohit/cryptoCMD.git',
        'datamine @ git+https://github.com/Saran33/datamine_python.git',
        'pykalman @ git+https://github.com/pykalman/pykalman.git',
        'pandas','numpy', 'scipy', 'pandas_summary','plotly','quandl','TA-Lib','ta','tqdm','pytz',
],
	#package_dir={"": "src"},
    #packages=find_packages(where="pwe"),
    python_requires=">=3.8",
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
