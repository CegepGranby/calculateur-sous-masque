#!/usr/bin/python3.6

import re
from ip_utils import *
from solution import ipcalc
from argparse import ArgumentParser
import json

def load_answers():
    def convert_to_ip_info(dic_str):
        dic = json.loads(dic_str)
        return IPInfo.from_dict(dic)

    frontier_ans = list(map(convert_to_ip_info, open('data/frontiere.txt').readlines()))
    non_frontier_str = list(map(convert_to_ip_info, open('data/non-frontiere.txt').readlines()))

    return (frontier_ans, non_frontier_str)

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
    parser.add_argument("-c", "--correcteur", dest="cor", action='store_true')
    args = parser.parse_args()

    # Mode correction
    if args.cor:
        frontier, non_frontier = load_answers()
        line = "\n" + "=" * 100 + "\n"
        print(line)
        print("Correcteur automatique, bonne chance!")
        print(line)

        def validate_student_answer(ans):
            ip_addr = parse_ip(ans.ip_addr)
            student_ans = ipcalc(ip_addr, gen_mask(ip_addr.mask_length))
            return ans == student_ans

        all_good = reduce(lambda x, y: x and y, list(map(validate_student_answer, frontier)), True)

        total_frontier = 2 if all_good else 0
        print(line)
        print("Total partie sur la frontière d'octet : {0}/2".format(total_frontier))
        print(line)

        all_good = reduce(lambda x, y: x and y, list(map(validate_student_answer, non_frontier)), True)

        total_non_frontier = 2 if all_good else 0
        print(line)
        print("Total partie pas sur une frontière d'octet : {0}/2".format(total_non_frontier))
        print(line)

        total = total_non_frontier + total_frontier
        if total == 4:
            total += 1
            print("Tout est bon, Bravo! Total++")
            print_gj()

        print("Total {0}/5".format(total))
        print(line)
        return

    addr = get_addr(args)

    # Voici le point d'entree de l'exercice, cette ligne appellera votre code.
    ipcalc(addr, gen_mask(addr.mask_length))


if __name__ + "__main__":
    main()