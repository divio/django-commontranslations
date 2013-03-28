from setuptools import setup, find_packages

version = __import__('django_commontranslations').__version__

setup(
    name = "django-commontranslations",
    version = version,
    url = 'http://github.com/divio/django-commontranslations',
    license = 'BSD',
    platforms=['OS Independent'],
    description = "prevents repeating translations across apps and projects",
    long_description = open('README.rst').read(),
    author = 'Stefan Foulis (Divio AG)',
    author_email = 'stefan@foulis.ch',
    packages=find_packages(),
    install_requires = (
        'Django>=1.3',
        'polib',
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
