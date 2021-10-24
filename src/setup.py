from setuptools import setup

setup(
	name='streamfinder',
	version='0.0',
	url='https://github.com/Adams475/Streaming-Service-Finder',
	license='AGPL',
	packages=['streamfinder'],
	package_data={'streamfinder': ['templates/*', 'static/*', 'static/css/*']},
	include_package_data=True,
	entry_points = {
		'console_scripts': [
			'streamfinder = streamfinder.__main__:main',
		]
	}
)

