from distutils.core import setup
files = []
setup(name = "plc-upo-alarm",
    version = "1.0",
    description = "Detect and emit a SNS message to a properly configured AWS account when a EoP intruder is detected",
    author = "alanbertadev",
    author_email = "alanbertadev@gmail.com",
    url = "alanbertadev.com",
    packages = ['package'],
    package_data = {'package' : files },
    scripts = ["plc-upo-alarm"],
    install_requires=[
        "boto"
    ]
) 
