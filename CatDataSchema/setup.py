from setuptools import setup, find_namespace_packages

with open("README.md", "r") as file:
    long_description = file.read()

with open("VERSION", "r") as version_file:
    version = version_file.read()

setup(
    name="kernel.test.schema",
    version=version,
    author="kernel",
    description="test schema package",
    url="https://git.kernel.corp/projects/MNT/repos/test-station-schema/browse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(include=["kernel.test.schema", "kernel.test.schema.*"]),
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines()[2:],
    entry_points={
        "console_scripts": [
            "test_data_watcher=kernel.test.schema.cli:test_data_watcher",
            "test_result_watcher=kernel.test.schema.cli:test_result_watcher",
            "kts-migrate=kernel.test.schema.cli:migrate",
        ]
    },
    package_data={"kernel.test.schema": []},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Database",
    ],
)
