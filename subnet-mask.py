#!/usr/bin/python3.6
# Ce fichier est un petit script Python servant a prendre une addresse IP et
# d'en extraire son masque sous-reseau, wildcard, etc...
import re
from argparse import ArgumentParser

ip_pattern = re.compile(r"^(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})\/(\d{1,2})$")


class IPAddress:
    byte_groups = [0, 0, 0, 0]
    mask_length = 32

    def __init__(self, byte_groups, mask_length):
        self.byte_groups = byte_groups
        self.mask_length = mask_length


def extract_byte(str):
    byte = int(str)
    if byte not in range(0, 255):
        err = ValueError()
        err.strerror = "Valeur d'octet invalide : {0}".format(byte)
        raise err

    return byte


def parse_ip(addr):
    valid_ip = re.match(ip_pattern, addr)
    if not valid_ip:
        err = ValueError()
        err.strerror = "EX : 113.92.12.133/12\n"
        raise err

    parsed_bytes = list(map(extract_byte, valid_ip.groups()[:-1]))

    mask_length = int(valid_ip.groups()[-1])
    if mask_length not in range(0, 32):
        err = ValueError()
        err.strerror = "Valeur de masque invalide : {0}".format(mask_length)
        raise err

    return IPAddress(parsed_bytes, mask_length)


def get_addr():
    parser = ArgumentParser()
    parser.add_argument("-a", "--adresse", dest="adr")

    args = parser.parse_args()

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
    addr = get_addr()
    print(addr)


if __name__ + "__main__":
    main()
