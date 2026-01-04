from setuptools import setup, find_packages

setup(
    name="chess-app",
    version="0.1.0",
    py_modules=["chess_app"],
    install_requires=[
        "pygame",
        "python-chess",
    ],
    entry_points={
        "console_scripts": [
            "chess=chess_app:main",
        ],
    },
)