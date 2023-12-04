import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name="HunYuanGPT",
    version="0.1.0",
    license="GPL-3.0",
    author="Zhangsheng Liao",
    author_email="liaozhangsheng@163.com",
    description="Reverse engineered HunYuan chat",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages("HunYuanGPT"),
    package_dir={"": "HunYuanGPT"},
    url="https://github.com/liaozhangsheng/HunYuanGPT",
    project_urls={
        "Bug Report": "https://github.com/liaozhangsheng/HunYuanGPT/issues/new"
    },
    entry_points={
        "console_scripts": [
            "hunyuan-gpt = HunYuanCLI:main",
        ],
    },
    install_requires=[
        "rich",
        "prompt_toolkit",
        "requests"
    ],
    keywords=["reverse-engineering", 
              "HunYuan", 
              "gpt"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11"
    ],
)
