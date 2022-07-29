from setuptools import setup, find_namespace_packages

with open("README.md", "r") as file:
    long_description = file.read()

with open("VERSION", "r") as version_file:
    version = version_file.read()

setup(
    name="CatDataSchema",
    version=version,
    author="Emma Li",
    description="cat data schema package",
    url="https://github.com/emma-jinger/CatWatcher/tree/main/CatDataSchema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(include=["CatDataSchema", "CatDataSchema.*"]),
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "cat_data_watcher=CatDataSchema.cli:cat_data_watcher",
            "cat_data_migrate=CatDataSchema.cli:migrate",
        ]
    },
    package_data={"CatDataSchema": []},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Database",
    ],
)
