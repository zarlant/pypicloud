""" Setup file """
from setuptools import setup, find_packages

import os
import re


HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, "README.rst")).read()
CHANGES = open(os.path.join(HERE, "CHANGES.rst")).read()
# Remove custom RST extensions for pypi
CHANGES = re.sub(r"\(\s*:(issue|pr|sha):.*?\)", "", CHANGES)
CHANGES = re.sub(r":ref:`(.*?) <.*>`", r"\1", CHANGES)

REQUIREMENTS = [
    "boto3>=1.7.0,<1.8",  # Hack until https://github.com/spulec/moto/issues/1793 is fixed
    # beaker needs this
    "cryptography",
    # We're doing enough subclassing and monkey patching to where we really do
    # need to lock this in to a specific version.
    "distlib==0.2.5",
    "paste",
    "passlib>=1.7",
    "pyramid",
    "pyramid_beaker",
    "pyramid_duh>=0.1.1",
    "pyramid_jinja2",
    "pyramid_rpc",
    "pyramid_tm",
    "six",
    "transaction",
    "zope.sqlalchemy",
]

EXTRAS = {
    "ldap": ["pyldap"],
    "dynamo": ["flywheel >= 0.2.0"],
    "redis": ["redis"],
    "gcs": ["google-cloud-storage>=1.10.0"],
}

EXTRAS["all_plugins"] = sum(EXTRAS.values(), [])

EXTRAS["test"] = EXTRAS["all_plugins"] + [
    "mock",
    "mockldap",
    "moto",
    "mysqlclient",
    "nose",
    "psycopg2-binary",
    "requests",
    "webtest",
]

EXTRAS["server"] = ["waitress"]
EXTRAS["lint"] = ["black", "pylint==2.1.1"]
EXTRAS["doc"] = ["numpydoc", "sphinx", "sphinx_rtd_theme"]


if __name__ == "__main__":
    setup(
        name="pypicloud",
        version="1.0.8",
        description="Private PyPI backed by S3",
        long_description=README + "\n\n" + CHANGES,
        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Development Status :: 4 - Beta",
            "Framework :: Pyramid",
            "Intended Audience :: System Administrators",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: System :: Systems Administration",
        ],
        license="MIT",
        author="Steven Arcangeli",
        author_email="stevearc@stevearc.com",
        url="http://pypicloud.readthedocs.org/",
        keywords="pypi s3 cheeseshop package",
        platforms="any",
        zip_safe=False,
        include_package_data=True,
        packages=find_packages(exclude=("tests",)),
        entry_points={
            "console_scripts": [
                "pypicloud-gen-password = pypicloud.scripts:gen_password",
                "pypicloud-make-config = pypicloud.scripts:make_config",
                "ppc-gen-password = pypicloud.scripts:gen_password",
                "ppc-make-config = pypicloud.scripts:make_config",
                "ppc-migrate = pypicloud.scripts:migrate_packages",
                "ppc-export = pypicloud.scripts:export_access",
                "ppc-import = pypicloud.scripts:import_access",
                "ppc-create-s3-sync = pypicloud.lambda_scripts:create_sync_scripts",
                "ppc-build-lambda-bundle = pypicloud.lambda_scripts:build_lambda_bundle",
            ],
            "paste.app_factory": ["main = pypicloud:main"],
        },
        install_requires=REQUIREMENTS,
        tests_require=REQUIREMENTS + EXTRAS["test"],
        test_suite="tests",
        extras_require=EXTRAS,
    )
