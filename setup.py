from setuptools import setup

setup(
    name='gradebook',
    version='0.19',
    license='BSD',
    packages=['gradebook', 'gradebook.tests'],
    entry_points=dict(console_scripts=[#'gb-assign = gradebook.assign:main',
                                       'gb-clone = gradebook.clone:main',
                                       #'gb-collect = gradebook.collect:main',
                                       #'gb-cp = gradebook.copy:main',
                                       #'gb-grades = gradebook.grades:main',
                                       #'gb-mkcsv = gradebook.mkcsv:main',
                                       'gb-run = gradebook.run:main',
                                       'gb-score = gradebook.score:main',
                                       'gb-stats = gradebook.stats:main',
                                       'gb-update = gradebook.update:main']),

)
