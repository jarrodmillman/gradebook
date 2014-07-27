from setuptools import setup

setup(
    name='score',
    version='0.11',
    packages=['gradebook'],
    entry_points=dict(console_scripts=['gb-score = gradebook.score:main']),
)
