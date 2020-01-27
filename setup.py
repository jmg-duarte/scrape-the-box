from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call


class PostInstallCommand(install):
    def run(self):
        check_call("sh build_fts5.sh .")
        install.run(self)


setup(
    name="scrape-the-box",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["click", "bs4", "requests",],
    entry_points="""
        [console_scripts]
        stb=stb.cli:cli
    """,
    author="José Duarte",
    author_email="jmg.duarte@campus.fct.unl.pt",
    description="A CLI tool to scrape the Hack the Box forum",
    keywords="scrape htb",
    url="https://github.com/jmg-duarte/scrape-the-box",
    project_urls={"Source Code": "https://github.com/jmg-duarte/scrape-the-box",},
    zip_safe=False,
)
