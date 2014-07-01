# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='etl_utils',
    version='0.0.2',
    url='http://github.com/mvj3/etl_utils/',
    license='MIT',
    author='David Chen',
    author_email=''.join(reversed("moc.liamg@emojvm")),
    description='etl utils',
    long_description='etl utils',
    packages=['etl_utils'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'fast_object_id >= 0.0.2',
        'nltk',
        'marisa_trie',
        'werkzeug',
        'lxml >= 3.3.5',
        'pyenchant',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
