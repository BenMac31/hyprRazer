import setuptools

from hyprrazer import __version__


def read_me():
    with open("README.md", "r") as f:
        return f.read()


setuptools.setup(
    name="hyprrazer",
    version=__version__,
    author="Benjamin McIntyre",
    author_email="",
    description="Shortcut/Command visualization on razer keyboards via openrazer",
    long_description=read_me(),
    long_description_content_type="text/markdown",
    url="https://github.com/benmac6/hyprRazer",
    packages=setuptools.find_packages(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        "xlib>=0.21",
        "PyYAML>=5.3.1"
    ],
    dependency_links=[  # not supported by pip, but the information is useful
        # openrazer should be installed manually, so the daemon and driver is installed
        "https://openrazer.github.io/#download"
    ],
    python_requires=">=3",
    entry_points={
        "console_scripts": [
            "hyprrazer=hyprrazer:main",
        ],
    },
)
