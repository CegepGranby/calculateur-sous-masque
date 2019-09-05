#!/usr/bin/python3.6

import re
from ip_utils import IPAddress, DecimalDotNotation, Byte
from ipcalc import ipcalc
from argparse import ArgumentParser

ip_pattern = re.compile(r"^(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})\/(\d{1,2})$")

def extract_byte(str):
    value = int(str)
    if value not in range(255):
        err = ValueError()
        err.strerror = "Valeur d'octet invalide : {0}".format(value)
        raise err

    return Byte(value)

def parse_ip(addr):
    valid_ip = re.match(ip_pattern, addr)
    if not valid_ip:
        err = ValueError()
        err.strerror = "EX : 113.92.12.133/12\n"
        raise err

    ddn = DecimalDotNotation.from_byte_groups(list(map(extract_byte, valid_ip.groups()[:-1])))

    mask_length = int(valid_ip.groups()[-1])
    if mask_length not in range(32):
        err = ValueError()
        err.strerror = "Valeur de masque invalide : {0}".format(mask_length)
        raise err

    return IPAddress(ddn, mask_length)

def get_addr(args):
    addr = None
    if args.adr:
        try:
            addr = parse_ip(args.adr)
        except ValueError as e:
            print("\nErreur de syntaxe pour l'adresse IP CIDR", e.strerror, sep="\n")

    while addr is None:

        user_input = input("----- Entrez une adresse IP CIDR : ----- \n")

        try:
            addr = parse_ip(user_input)
        except ValueError as e:
            print("\n> Erreur de syntaxe pour l'adresse IP CIDR", e.strerror, sep="\n> ")

    return addr


def main():
    parser = ArgumentParser()
    parser.add_argument("-a", "--adresse", dest="adr")
    args = parser.parse_args()

    addr = get_addr(args)

    mask = ~(-1 << addr.mask_length) << (32 - addr.mask_length)

    ipcalc(addr, DecimalDotNotation.from_dec(mask))


if __name__ + "__main__":
    main()