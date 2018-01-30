# -*- coding:utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.0b3'
description = 'A Photo Gallery content type with a slideshow view.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='sc.photogallery',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone photo gallery content type dexterity',
    author='Simples Consutoria',
    author_email='produtos@simplesconsultoria.com.br',
    url='https://github.com/collective/sc.photogallery',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['sc'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.js.cycle2',
        'plone.api',
        'plone.app.dexterity [relations]',
        'plone.app.relationfield',
        'plone.app.textfield',
        'plone.app.upgrade',
        'plone.dexterity',
        'plone.memoize',
        'plone.supermodel',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.robotframework',
            'plone.app.testing [robot]',
            'plone.browserlayer',
            'plone.testing',
            'plone.uuid',
            'robotsuite',
            'zope.component',
        ],
        'zipexport': [
            'ftw.zipexport',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
