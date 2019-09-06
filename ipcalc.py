#!/usr/bin/python3.6

import re
from ip_utils import IPAddress, DecimalDotNotation, Byte
from solution import ipcalc
from argparse import ArgumentParser

# Expression reguliere pour valider et extraire chacune des valeurs
ip_pattern = re.compile(r"^(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})\/(\d{1,2})$")

# Transforme un string en objet IPAdress
def parse_ip(addr):
    valid_ip = re.match(ip_pattern, addr)
    if not valid_ip:
        err = ValueError()
        err.strerror = "EX : 113.92.12.133/12\n"
        raise err

    # Valide une valeur decimale et la transforme en objet Byte
    def extract_byte(str):
        value = int(str)
        # On valide que notre octet est entre 0 et 255
        if value not in range(256):
            err = ValueError()
            err.strerror = "Valeur d'octet invalide : {0}".format(value)
            raise err

        return Byte(value)

    ddn = DecimalDotNotation.from_byte_groups(list(map(extract_byte, valid_ip.groups()[:-1])))

    # Valide que le masque est une valeur entre 0 et 32
    mask_length = int(valid_ip.groups()[-1])
    if mask_length not in range(33):
        err = ValueError()
        err.strerror = "Valeur de masque invalide : {0}".format(mask_length)
        raise err

    return IPAddress(ddn, mask_length)

# Fonction prenant les entrees de l'utilisateur jusqu'a temps qu'il donne une adresse
# IP valide
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

    # Cree un bitmask rempli de 1 de longeur n (la taille de notre masque)
    # Demonstration avec une longeur de 8 bits:
    #   > 1                  = 0000 0000 0001
    #   > 1 << 8 = 256       = 0001 0000 0000
    #                               <<<<8<<<<
    #   > (1 << 8) - 1 = 255 = 0000 1111 1111
    mask = (1 << addr.mask_length) - 1

    # Decale le masque de (32 - n) bits vers la gauche pour le positionner a la bonne place
    #   > 255               = 0000 0000 0000 0000 0000 0000 1111 1111
    #   > 255 << (32 - 8)
    #   > 255 << 26         = 1111 1111 0000 0000 0000 0000 0000 0000
    #                                   <<<<<<<<<<<26<<<<<<<<<<<<<<<<
    mask = mask << (32 - addr.mask_length)

    # Voici le point d'entree de l'exercice, cette ligne appellera votre code.
    ipcalc(addr, DecimalDotNotation.from_dec(mask))


if __name__ + "__main__":
    main()