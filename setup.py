from setuptools import setup, find_packages


setup(
    name="scrape-the-box",
    version="0.2.1",
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
