def luhn_mod_n(mode, barcode, alphabet):
    # Adapted for Python from examples at https://en.wikipedia.org/wiki/Luhn_mod_N_algorithm

    if mode == "generate":
        factor = 2
    elif mode == "validate":
        factor = 1 # Factor starts at 1 as rightmost char is check digit now
    else:
        return None

    csum = 0
    alphabet_n = len(alphabet)

    # Staring from the right work leftwards through the barcode
    for i in reversed(range(len(barcode))):
        code_point = alphabet.index(barcode[i].lower())
        addend = int(factor * code_point)

        # Flip the factor
        factor = 1 if factor == 2 else 2

        # Sum addend in base n
        addend = (addend / alphabet_n) + (addend % alphabet_n)
        addend = int(addend)
        csum += addend

    remainder = int(csum % alphabet_n)

    if mode == "generate":
        # Calculate the number that must be added to sum to make it divisible by n
        # Return the checksum as int and alphabet char
        check_int = int((alphabet_n - remainder) % alphabet_n)
        return check_int, alphabet[check_int]

    elif mode == "validate":
        # Remainder should be zero
        return remainder == 0

    else:
        # ???
        return None

CHECKSUMS = {
    "luhn_mod_n": luhn_mod_n,
    None: None,
}
