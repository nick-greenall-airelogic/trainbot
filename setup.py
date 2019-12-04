from setuptools import setup, find_packages

setup(
    name='Trainbot',
    version=0.1,
    description='A little bot to get train times and post to slack',
    packages=find_packages(),
    install_requires=[
        'nre-darwin-py',
        'slackclient',
    ],
    entry_points={
        'console_scripts': [
            'trainbot = trainbot.main:run',
        ]
    },
)
