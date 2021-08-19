# *********************************************
# Copyright (C) 2021 Meemo <meemo4556@gmail.com> - All Rights Reserved
#
# Unauthorized copying of this file, via any medium is strictly prohibited
#
# Proprietary and confidential
# *********************************************

import re
from textwrap import wrap


# Converts KWZ format FSIDs to PPM format.
# KWZ format FSIDs must be 18 or 20 characters.
# Any invalid input will be returned without modification.
# - e.g. if a PPM format FSID is used as the input or the length is invalid
def ConvertKWZtoPPM(input_fsid):
    output_fsid = ""

    if re.match("[0159][0-9A-F]{15}(00)?", input_fsid) is not None:
        # Trim the first byte of the FSID
        # FSIDs from KWZ files have an extra null(?) byte at the end, trim it if it exists
        if len(input_fsid) == 20:
            input_fsid = input_fsid[2:-2]
        else:
            input_fsid = input_fsid[2:]

        # Invert the FSID then split into byte sized chunks
        string_list = wrap(input_fsid[::-1], 2)

        # Invert each byte and append to the output string
        for i in range(len(string_list)):
            output_fsid += string_list[i][::-1]
    else:
        output_fsid = input_fsid

    return output_fsid


# Converts PPM format FSIDs to KWZ format
# The first byte appears to be useless, as all versions (00, 10, 12, 14) refer to the same user
# This returns the FSID with 00 as the leading byte by default
# The trailing null byte is also included
def ConvertPPMtoKWZ(input_fsid):
    if len(input_fsid) == 16 and re.match("[0159][0-9A-F]{15}", input_fsid) is not None:
        output_fsid = ""

        # Invert the FSID then split into byte sized chunks
        string_list = wrap(input_fsid[::-1], 2)

        # Invert each byte and append to the output string
        for i in range(len(string_list)):
            output_fsid += string_list[i][::-1]

        return "00" + output_fsid + "00"
    else:
        return ""


# Verifies that the FSID is
def VerifyPPMFSID(input_fsid):
    return re.match("[0159][0-9A-F]{15}", input_fsid) is not None


def VerifyKWZFSID(input_fsid):
    return re.match("(00|10|12|14)[0-9A-F]{14}[0159][0-9A-F](00)?", input_fsid) is not None
