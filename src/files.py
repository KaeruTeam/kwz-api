import re


def VerifyFilename(name):
    return re.match("[a-z0-5]{28}", name) is not None
