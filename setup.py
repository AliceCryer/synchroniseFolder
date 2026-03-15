import setuptools

setuptools.setup(
    name="synchroniseFolder",
    version="0.1.0",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=["destinationAPI", "main"],
    test_suite="test",
    install_requires=[],
    extras_require={
        "dev": ["pytest", "pytest-cov"]
    },
)