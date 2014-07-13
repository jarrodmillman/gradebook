from setuptools import setup

setup(
    name='score',
    version='0.1',
    py_modules=['score'],
    entry_points=dict(console_scripts=['gb-score = score:main']),
)
