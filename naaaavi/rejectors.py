import sys

def max_repeats(int_barcode, str_barcode, conf):
    max_repeats = int(conf[0])

    last_val = None
    last_len = 1 # start with run of 1 to include first pos
    for b in int_barcode:
        if last_val is not None:
            if last_val == b:
                last_len += 1
        last_val = b

        if last_len > max_repeats:
            return True # return true to reject
    return False

def min_unique(int_barcode, str_barcode, conf):
    min_unique = int(conf[0])

    if len(set(int_barcode)) < min_unique:
        return True
    return False

def avoid_ismp_flips(barcode, str_barcode, conf):
    # This will reject barcodes that contain any adjacent pairs listed in
    # the Institute for Safe Medication Practices list of commonly confused symbols
    # https://www.ismp.org/resources/misidentification-alphanumeric-symbols
    # Note that cursive confusion is excluded. Table is case-sensitive but we'll
    # toss out any pair in a barcode as it could be written in upper or lower case.
    symbols = [
        "TI", "IT",
        "DO", "OD",
        "CG", "GC",
        "LI", "IL",
        "MN", "NM",
        "PB", "BP",
        "FR", "RF",
        "UO", "OU",
        "UV", "VU",
        "EF", "FE",
        "VW", "WV",
        "XY", "YX",
        "G6", "6G",
        "F7", "7F",
        "Z2", "2Z",
        "Q2", "2Q",
        "O0", "0O",
        "B8", "8B",
        "D0", "0D",
        "S5", "5S",
        "S8", "8S",
        "Y5", "5Y",
        "Z7", "7Z",
        "U0", "0U",
        "U4", "4U",

        "gq", "qg",
        "pn", "np",
        "mn", "nm",
        "yz", "zy",
        "ce", "ec",

        "08", "80",
        "39", "93",
        "38", "83",
        "49", "94",
        "58", "85",
        "53", "35",
        "68", "86",
        "71", "17",
    ]
    for bad_symbol in symbols:
        if bad_symbol.lower() in str_barcode.lower():
            return True
    return False


REJECTORS = {
    "max_repeats": max_repeats,
    "min_unique": min_unique,
    "ismp_flips": avoid_ismp_flips,
}
