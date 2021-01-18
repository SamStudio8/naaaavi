import sys

def max_repeats(barcode, conf):
    max_repeats = int(conf[0])

    last_val = None
    last_len = 1 # start with run of 1 to include first pos
    for b in barcode:
        if last_val is not None:
            if last_val == b:
                last_len += 1
        last_val = b

        if last_len > max_repeats:
            return True # return true to reject
    return False

def min_unique(barcode, conf):
    min_unique = int(conf[0])

    if len(set(barcode)) < min_unique:
        return True
    return False

REJECTORS = {
    "max_repeats": max_repeats,
    "min_unique": min_unique,
}
