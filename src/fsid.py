import re
from sys import argv
from textwrap import wrap


# Converts KWZ format FSIDs to PPM format.
# KWZ format FSIDs must be 18 or 20 characters. "" will be returned if the length is invalid.
# If a PPM format FSID is used as the input, it will be returned without modification.
def convertFSID(input_fsid):
    output_fsid = ""

    if len(input_fsid) > 16:
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
    elif len(input_fsid) == 16 and re.match("[0159][0-9A-F]{15}", input_fsid) is not None:
        # Matches length and regex, no need to convert
        output_fsid = input_fsid

    return output_fsid


def validateFSID(fsid):
    if len(fsid) == 16:
        return re.match("[0159][0-9A-F]{15}", fsid) is not None

    elif len(fsid) == 18 or len(fsid) == 20:
        return re.match("[0159][0-9A-F]{15}", convertFSID(fsid)) is not None

    else:
        return False


if __name__ == "__main__":
    print(convertFSID(argv[1]))
