from setuptools import setup

setup(
    name='gradebook',
    version='0.12',
    license='BSD',
    packages=['gradebook'],
    entry_points=dict(console_scripts=['gb-score = gradebook.score:main',
                                       'gb-stats = gradebook.stats:main']),

)
