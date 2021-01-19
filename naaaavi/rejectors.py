import os
import sys

class NaviRejector:
    def __init__(self, conf):
        self.conf = str(','.join(conf))

    def handle_barcode(self, int_barcode, str_barcode):
        pass

    def get_log_line(self):
        return "%s:%s" % (self.name, self.conf)


class Rejector_MaxRepeats(NaviRejector):
    def __init__(self, conf):
        self.name = "max_repeats"
        self.max_repeats = int(conf[0])
        super().__init__(conf)

    def handle_barcode(self, int_barcode, str_barcode):
        last_val = None
        last_len = 1 # start with run of 1 to include first pos
        for b in int_barcode:
            if last_val is not None:
                if last_val == b:
                    last_len += 1
            last_val = b

            if last_len > self.max_repeats:
                return True # return true to reject
        return False


class Rejector_MinUnique(NaviRejector):
    def __init__(self, conf):
        self.name = "min_unique"
        self.min_unique = int(conf[0])
        super().__init__(conf)

    def handle_barcode(self, int_barcode, str_barcode):
        if len(set(int_barcode)) < self.min_unique:
            return True
        return False


class Rejector_ISMPFlips(NaviRejector):
    def __init__(self, conf):
        # This will reject barcodes that contain any adjacent pairs listed in
        # the Institute for Safe Medication Practices list of commonly confused symbols
        # https://www.ismp.org/resources/misidentification-alphanumeric-symbols
        # Note that cursive confusion is excluded. Table is case-sensitive but we'll
        # toss out any pair in a barcode as it could be written in upper or lower case.
        self.name = "ismp_flips"
        self.symbols = [
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
        super().__init__(conf)

    def handle_barcode(self, int_barcode, str_barcode):
        for bad_symbol in self.symbols:
            if bad_symbol.lower() in str_barcode.lower():
                return True
        return False


class Rejector_Banlist(NaviRejector):
    def __init__(self, conf):
        self.name = "ban_list"
        self.path = conf[0]
        self.entries = []
        super().__init__(conf)

        if not os.path.exists(self.path):
            sys.stderr.write("[FAIL] Could not open ban_list %s\n" % self.path)
            self.conf = ""
            return

        self.name = os.path.basename(self.path)

        # Hash for log
        import hashlib
        hash_md5 = hashlib.md5()
        with open(self.path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        self.hash = hash_md5.hexdigest()

        # Now open again for the list itself
        with open(self.path, "r") as f:
            for line in f:
                self.entries.append(line.strip())

        self.entries = set(self.entries)

        # Override conf string
        self.conf = "%s@%d@%s" % (self.name, len(self.entries), self.hash)

    def handle_barcode(self, int_barcode, str_barcode):
        for banned in self.entries:
            if banned.lower() in str_barcode.lower():
                return True
        return False

REJECTORS = {
    "max_repeats": Rejector_MaxRepeats,
    "min_unique": Rejector_MinUnique,
    "ismp_flips": Rejector_ISMPFlips,
    "ban_list": Rejector_Banlist,
}
