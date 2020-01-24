from setuptools import setup

setup(
    name="scrape-the-box",
    version="0.2.0",
    pymodules=["stb"],
    include_package_data=True,
    install_required=["click", "bs4", "requests",],
    entry_points="""
        [console_scripts]
        stb=stb.cli:cli
    """,
)
