from distutils.core import setup

setup(
    name='PyPDFLite',
    version='0.1.41',
    author='Katerina Hanson',
    author_email='katerina.hanson@gmail.com',
    packages=['pypdflite', 'pypdflite.pdfobjects'],
    scripts=['runexamples.py'],
    license='LICENSE.md',
    description='Simple PDF Writer for Python 3',
    long_description=open('README.txt').read(),
    url='https://github.com/katerina7479/pypdflite',
    download_url='https://github.com/katerina7479/pypdflite/tarball/0.1'
)
