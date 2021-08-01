from textwrap import wrap

# This file contains functions pertaining to Flipnote Studio ID manipulation


# Converts KWZ format FSIDs to PPM format.
def kwzToPPM(input_fsid):
    output_fsid = ""

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

    return output_fsid
