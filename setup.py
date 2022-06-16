import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
with open("requirements.txt", "r") as requirements_file:
    requirements.append(requirements_file.read())

    #   1 - Planning
    #   2 - Development
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable

classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    "Intended Audience :: Developers",
    "Topic :: Communications",
    "Topic :: Utilities",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]

setuptools.setup(
    name="loki-assistant",
    version="0.0.2",
    author="Uwe Roder",
    author_email="uweroder@gmail.com",
    description="The LokiAssistant lib is a small tool to push logging to Loki server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grobbles/LokiAssistant",
    packages=["loki_assistant"],
    license='MIT',
    classifiers=classifiers,
    python_requires='>=3.7',
    keywords=["loki_assistant", "Loki", "Assistant", "Grafana"],
    install_requires=requirements
)
