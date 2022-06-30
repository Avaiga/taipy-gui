#!/usr/bin/env python

# Copyright 2022 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""The setup script."""

import os
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py

with open("README.md") as readme_file:
    readme = readme_file.read()


requirements = [
    "flask>=2.1,<3.0",
    "flask-cors>=3.0.10,<4.0",
    "flask-socketio>=5.1.1,<6.0",
    "markdown>=3.3.4,<4.0",
    "pandas>=1.3.4,<2.0",
    "python-dotenv>=0.19,<0.21",
    "pytz>=2021.3,<2022.2",
    "simple-websocket>=0.3,<0.6",
    "tzlocal>=3.0,<5.0",
    "backports.zoneinfo>=0.2.1,<0.3;python_version<'3.9'",
    "flask-talisman>=1.0,<2.0",
]

test_requirements = ["pytest>=3.8"]

extras_require = {
    "ngrok": ["pyngrok>=5.1,<6.0"],
    "image": ["python-magic>=0.4.24,<0.5;platform_system!='Windows'", "python-magic-bin>=0.4.14,<0.5;platform_system=='Windows'"],
    "rdp": ["rdp>=0.8"],
    "arrow": ["pyarrow>=7.0,<9.0"],
}


def _build_webapp():
    already_exists = Path(f"./taipy/gui/webapp/index.html").exists()
    if not already_exists:
        os.system("cd gui && npm ci && npm run build")


class NPMInstall(build_py):
    def run(self):
        _build_webapp()
        build_py.run(self)


setup(
    author="Avaiga",
    author_email="dev@taipy.io",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="An Open Source GUI generator for Python that need no knowledge of Web application development.",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    license="Apache License 2.0",
    include_package_data=True,
    keywords="taipy-gui",
    name="taipy-gui",
    packages=find_packages(include=["taipy", "taipy.gui", "taipy.gui.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/avaiga/taipy-gui",
    version="1.1.1",
    zip_safe=False,
    extras_require=extras_require,
    cmdclass={"build_py": NPMInstall},
)
