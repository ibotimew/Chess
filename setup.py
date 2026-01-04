from setuptools import setup

setup(
    name="chess-app",
    version="0.1.0",
    py_modules=["chess_app"],
    python_requires=">=3.9",
    install_requires=[
        "pygame",
        "python-chess",
    ],
    entry_points={
        "console_scripts": [
        "offline-chess=chess_app:main",
    ],
    },
)
