from setuptools import setup

setup(
    name='gradebook',
    version='0.13',
    license='BSD',
    packages=['gradebook'],
    entry_points=dict(console_scripts=['gb-clone = gradebook.clone:main',
                                       'gb-score = gradebook.score:main',
                                       'gb-stats = gradebook.stats:main',
                                       'gb-update = gradebook.update:main']),

)
