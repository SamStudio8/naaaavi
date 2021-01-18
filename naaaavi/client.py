import argparse
import sys

from naaaavi.version import __version__
from naaaavi.alphabets import ALPHABETS as NAVI_ALPHABETS
from naaaavi.checksums import CHECKSUMS as NAVI_CHECKSUMS
from naaaavi.rejectors import REJECTORS as NAVI_REJECTORS

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action='version', version="naaaavi v%s" %  __version__)

    action_parser = parser.add_subparsers(dest='command')

    generate_parser = action_parser.add_parser("generate")
    generate_parser.add_argument("--alphabet", required=True)
    generate_parser.add_argument("--checksum", required=False)
    generate_parser.add_argument("--size", required=True, type=int)
    generate_parser.add_argument("-n", required=False, type=int, default=1)
    generate_parser.add_argument("--rejectors",  nargs='+', required=False)

    generate_parser.add_argument("--last-code", required=False, type=str, default=None)

    generate_parser.add_argument("--prefix", required=False, type=str, default="")
    generate_parser.add_argument("--upper", required=False, action="store_true",
            help="Force uppercase characters if you want to feel like you are stuck in an 1980s terminal")

    validate_parser = action_parser.add_parser("validate")
    validate_parser.add_argument("--barcodes",  nargs='+', required=True)
    validate_parser.add_argument("--alphabet", required=True)
    validate_parser.add_argument("--checksum", required=True)

    args = parser.parse_args()
    #print("Hey listen!")

    ok = True
    alphabet = None
    checksum = None

    if args.alphabet.lower() not in NAVI_ALPHABETS:
        sys.stderr.write("[FAIL] Alphabet '%s' not in alphabets\n" % args.alphabet)
        ok = False
    else:
        alphabet = NAVI_ALPHABETS[args.alphabet.lower()]

    if args.checksum and args.checksum.lower() not in NAVI_CHECKSUMS:
        sys.stderr.write("[FAIL] Checksum '%s' not in checksums\n" % args.checksum)
        ok = False
    else:
        checksum = NAVI_CHECKSUMS[args.checksum.lower()]

    rejectors_d = {}
    if hasattr(args, "rejectors"):
        if args.rejectors:

            for rejector in args.rejectors:
                rejector_name, rejector_conf = rejector.lower().split(':')
                if rejector_name not in NAVI_REJECTORS:
                    sys.stderr.write("[FAIL] Rejector '%s' not in rejectors\n" % rejector_name)
                    ok = False
                else:
                    rejectors_d[rejector_name] = rejector_conf.split(',')

    if not ok:
        sys.exit(1)

    if args.command == "generate":
        navi_generate(alphabet, args.size, args.n, checksum, args, rejectors=rejectors_d)
    elif args.command == "validate":
        navi_validate(args.barcodes, alphabet, checksum, args)
    else:
        sys.exit(2)


def _gen_increment_barcode_positions(barcode, i, alphabet):
    try:
        barcode[i] += 1
    except IndexError:
        sys.stderr.write("[FAIL] Barcode space appears to have been exhausted. Larger --size required.\n")
        sys.exit(3)

    if barcode[i] >= len(alphabet):
        barcode[i] = 0
        barcode = _gen_increment_barcode_positions(barcode, i-1, alphabet)

    return barcode

def navi_generate(alphabet, size, rounds, checksum, args, rejectors={}):
    n_gen_total = 1
    n_gen_valid = 0

    if args.last_code:
        # Map the last barcode to code point space and increment it to start
        sys.stderr.write("[WARN] You have provided last_code %s. This MUST NOT have a check digit to start from the correct last position.\n" % args.last_code)
        last_barcode = args.last_code.split("-", 1)[-1].replace('.', '').replace('-', '')
        candidate_barcode = [ alphabet.index(b.lower()) for b in last_barcode ]
        candidate_barcode = _gen_increment_barcode_positions(candidate_barcode, -1, alphabet)
    else:
        candidate_barcode = [0] * size

    # Attempt to generate n rounds of barcodes, but abort if we've spent more than n_rounds*1000
    while n_gen_valid < rounds:
        valid = True # assume this candidate is not garbage

        # Test if the candidate is garbage
        for rejector_name, rejector_conf in rejectors.items():
            reject_func = NAVI_REJECTORS[rejector_name]
            if reject_func(candidate_barcode, rejector_conf):
                valid = False
                break # bail on the first sign this barcode is trash

        if valid:
            # Convert barcode candidate to string
            str_barcode = "".join([alphabet[i] for i in candidate_barcode])

            # Generate checksum if required
            check_int = None
            check_char = ""
            if checksum:
                try:
                    check_int, check_char = checksum("generate", str_barcode, alphabet)
                except Exception as e:
                    sys.stderr.write("[FAIL] Could not generate %s checksum for barcode %s. Exception: %s\n" % (args.checksum, str_barcode, str(e)))
                    sys.exit(2)

            if args.upper:
                str_barcode = str_barcode.upper()
                check_char = check_char.upper()

            # Count and output
            n_gen_valid += 1
            sys.stdout.write('\t'.join([
                args.prefix + str_barcode,
                check_char,
                args.alphabet,
                args.checksum,
                ';'.join(["%s=%s" % (k, v) for k, v in rejectors.items()]),
                __version__,
            ]) + '\n')


        # Increment barcode
        candidate_barcode = _gen_increment_barcode_positions(candidate_barcode, -1, alphabet)
        n_gen_total += 1

        if n_gen_total > (rounds * 1000000):
            sys.stderr.write("[WARN] Failed to generate the set number of barcodes. Your rejectors may be too restrictive.\n")
            break
    
    pass

def navi_validate(barcodes, alphabet, checksum, args):
    for barcode in barcodes:
        # Sanity check the barcode
        check_barcode = barcode.split("-", 1)[-1].replace('.', '').replace('-', '')

        status = None
        for b in check_barcode:
            # Don't bother validating a barcode with luhn if the char is invalid
            if b.lower() not in alphabet:
                status = -1
                sys.stdout.write('\t'.join([
                    barcode,
                    str(status),
                ]) + '\n')

        if status:
            continue

        result = checksum("validate", check_barcode, alphabet)
        if result is True:
            status = 1
        elif result is False:
            status = 0
        else:
            result = -1
        sys.stdout.write('\t'.join([
            barcode,
            str(status),
        ]) + '\n')
