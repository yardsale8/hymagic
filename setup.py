from distutils.core import setup
setup(
    name = 'hymagic',
    packages = ['hymagic'], # this must be the same as the name above
    version = '0.1',
    description = 'IPython magic for hylang',
    author = 'Todd Iverson',
    author_email = 'tiverson@smumn.edu',
    url = 'https://github.com/yardsale8/hymagic',   # use the URL to the github repo
    download_url = 'https://github.com/yardsale8/hymagic/tarball/0.1', # I'll explain this in a second
    keywords = ['hylang', 'IPython extension', 'IPython magic'], # arbitrary keywords
    classifiers = ["Development Status :: 3 - Alpha"],
)