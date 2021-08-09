import re


def VerifyKWZFilename(name):
    return re.match("[a-z0-5]{28}", name) is not None
