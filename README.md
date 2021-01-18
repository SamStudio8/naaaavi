# naaaavi
Naming avoiding ambiguity automatically assigning valid identifiers


## What is it?

`Naaaavi` (pronounced `nah-vee` as if someone hadn't injected a load of ambiguous confusing `a` characters) is a simple Python tool for generating identifiers.
It attempts to generate identifiers that:

* uses a character set (or other system) that aims to be human-friendly
* can be checksummed
* avoids ambiguity by testing the identifier against several `rejectors`
* are somewhat chronologically sortable
* are generated in a predictable fashion

It generates human-friendly identifiers using `diceware` (soon) or the `zbase32` alphabet, and allows for screening of common sources of confusion such as look-alike pairs and repetitive characters.

## What is it not?

`Naaaavi` does not:

* randomly generate identifiers
* encode anything into the identifiers
* generate universally or globally unique identifiers


## How do I use it?

### Generate barcodes

    $ naaaavi generate --alphabet zbase32 --checksum luhn_mod_n --size 6 --rejectors max_repeats:2 -n 10 --upper --prefix 'HOOT-'
    HOOT-YYBYBY     6       zbase32 luhn_mod_n      max_repeats=['2']       0.1.0

### Validate barcodes

    $ naaaavi validate --alphabet zbase32 --checksum luhn_mod_n --barcodes HOOT-YYBYBY.6 HOOT-YYBYBY6 YYBYBY6 YYBXBY6 YYBYBY7
    HOOT-YYBYBY.6   1
    HOOT-YYBYBY6    1
    YYBYBY6 1
    YYBXBY6 0
    YYBYBY7 0

### I don't like your funny command name

The `navi` command is provided as a synonym of `naaaavi` so you don't have to remember that there are currently four `a` characters in `naaaavi`.
