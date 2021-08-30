from re import compile

# Compile both regex, gives a minor performance increase.
KWZ = compile("[a-z0-5]{28}")
PPM = compile("[0-9A-F]{6}_[0-9A-F]{13}_[0-9]{3}")
PPM_FS = compile("[0-9A-Z][0-9A-F]{5}_[0-9A-F]{13}_[0-9]{3}")


def VerifyKWZFilename(name):
    return KWZ.match(name) is not None


def VerifyPPMFilename(name):
    return PPM.match(name) is not None


# PPM filenames in the filesystem (outside of file meta) have the first character used as a checksum
def VerifyPPMFilesystemName(name):
    return PPM_FS.match(name) is not None
