from setuptools import setup

setup(
    name="pyrocketbot",
    version="0.0.1",
    url="https://github.com/seyed-dev/rocketpybot",
    license="MIT",
    author="SeYeD Mohammad Khoshnava | seyed.dev",
    author_email="me@seyed.dev",
    description="Python lib for create rocket.chat bot with getupdate like TelegramBots",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    install_requires=("rocketchat-API",),
)
