import setuptools


setuptools.setup(
    name='peopleai-api',
    version='0.0.4',

    author='Max Zheng',
    author_email='maxzheng.os@gmail.com',

    description="Python library to download activities from People.ai's REST API",
    long_description=open('README.rst').read(),

    url='https://github.com/maxzheng/peopleai-api',

    install_requires=open('requirements.txt').read(),

    license='MIT',

    packages=setuptools.find_packages(),
    include_package_data=True,

    python_requires='>=3.6',
    setup_requires=['setuptools-git', 'wheel'],

    # Standard classifiers at https://pypi.org/classifiers/
    classifiers=[
      'Development Status :: 5 - Production/Stable',

      'Intended Audience :: Developers',
      'Topic :: Software Development :: Libraries',

      'License :: OSI Approved :: MIT License',

      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.6',
    ],

    keywords='People.ai activities API',
)
