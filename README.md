# naaaavi
Naming avoiding ambiguity automatically assigning valid identifiers


## What is it?

`Naaaavi` (pronounced `nah-vee` as if someone hadn't injected a load of ambiguous confusing `a` characters) is a simple Python tool for generating identifiers.
It attempts to generate identifiers that:

* use a character set (or other system) that aims to be human-friendly
* can be checksummed
* avoid ambiguity by testing the identifier against several `rejectors`
* are somewhat chronologically sortable
* are generated in a predictable fashion

It generates human-friendly identifiers using `diceware` (soon) or the `zbase32` alphabet, and allows for screening of common sources of confusion such as look-alike pairs and repetitive characters. `Naaaavi` also provides limited support for generating `ZPL` to print your nice new identifiers.

## What is it not?

`Naaaavi` does not:

* randomly generate identifiers
* encode anything into the identifiers
* generate universally or globally unique identifiers


## How do I use it?

### Generate identifiers

    $ naaaavi generate --alphabet zbase32 --checksum luhn_mod_n --size 5 --rejectors max_repeats:2 min_unique:3 ismp_flips: better_profanity: -n 10 --prefix 'HOOT-' --upper
    HOOT-YYBYN4     HOOT-YYBYN      4       zbase32 luhn_mod_n      max_repeats:2;min_unique:3;ismp_flips:;better_profanity:        0.4.1
    HOOT-YYBYDA     HOOT-YYBYD      A       zbase32 luhn_mod_n      max_repeats:2;min_unique:3;ismp_flips:;better_profanity:        0.4.1
    HOOT-YYBYRS     HOOT-YYBYR      S       zbase32 luhn_mod_n      max_repeats:2;min_unique:3;ismp_flips:;better_profanity:        0.4.1
    HOOT-YYBYFW     HOOT-YYBYF      W       zbase32 luhn_mod_n      max_repeats:2;min_unique:3;ismp_flips:;better_profanity:        0.4.1
    HOOT-YYBYG1     HOOT-YYBYG      1       zbase32 luhn_mod_n      max_repeats:2;min_unique:3;ismp_flips:;better_profanity:        0.4.1
    HOOT-YYBY8O     HOOT-YYBY8      O       zbase32 luhn_mod_n      max_repeats:2;min_unique:3;ismp_flips:;better_profanity:        0.4.1
    HOOT-YYBYEQ     HOOT-YYBYE      Q       zbase32 luhn_mod_n      max_repeats:2;min_unique:3;ismp_flips:;better_profanity:        0.4.1
    HOOT-YYBYJC     HOOT-YYBYJ      C       zbase32 luhn_mod_n      max_repeats:2;min_unique:3;ismp_flips:;better_profanity:        0.4.1
    HOOT-YYBYKK     HOOT-YYBYK      K       zbase32 luhn_mod_n      max_repeats:2;min_unique:3;ismp_flips:;better_profanity:        0.4.1
    HOOT-YYBYME     HOOT-YYBYM      E       zbase32 luhn_mod_n      max_repeats:2;min_unique:3;ismp_flips:;better_profanity:        0.4.1

### Validate identifiers

    $ naaaavi validate --alphabet zbase32 --checksum luhn_mod_n --barcodes HOOT-YYBYN.4 HOOT-YYBYN4 YYBYN4 YYBYM4 YYBYN5
    HOOT-YYBYN.4    1
    HOOT-YYBYN4     1
    YYBYN4  1
    YYBYM4  0
    YYBYN5  0

## Rejectors

* `max_repeats` will reject any identifier which repeats a particular symbol more than `n` times consecutively
* `min_unique` will reject any identifier that does not have at least `n` unique characters
* `ismp_flips` will reject any identifier that has at least one look alike pair noted as potentially confusing by the Institute for Safe Medication Practices
* `ban_list` will reject any identifier that has a prefix or suffix in your list
* `regex_list` will reject any identifier that searches positive against a list of regular expressions
* `better_profanity` (requires `pip install better_profanity`) will overzealously reject any identifier that could be mildly amusing

## Notes

### I work in COG and would love to use this too!

`Naaaavi` does not generate globally or universally unique identifiers, so please get in touch to make sure our (identifier) worlds don't collide.

### I don't like your funny command name

The `navi` command is provided as a synonym of `naaaavi` so you don't have to remember that there are currently four `a` characters in `naaaavi`.
