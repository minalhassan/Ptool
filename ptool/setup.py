from setuptools import setup, find_packages

setup(
    name="ptool",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer[all]==0.9.0",
        "rich==13.7.0",
        "google-generativeai==0.3.2",
        "pyperclip==1.8.2",
        "python-dotenv==1.0.0",
        "pydantic==2.5.3",
        "prompt_toolkit==3.0.43",
    ],
    entry_points={
        "console_scripts": [
            "ptool=ptool.main:app",
        ],
    },
    author="PTool Team",
    description="AI-Powered Penetration Testing CLI Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)