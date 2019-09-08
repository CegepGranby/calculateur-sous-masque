#!/usr/bin/python3.6

from ip_utils import IPAddress
from solution import ipcalc
from argparse import ArgumentParser
from functools import reduce
import json

# Fonction prenant les entrees de l'utilisateur jusqu'a temps qu'il donne une adresse
# IP valide
def get_addr(args):
    addr = None
    if args.adr:
        try:
            addr = IPAddress.from_str(args.adr)
        except ValueError as e:
            print("\nErreur de syntaxe pour l'adresse IP CIDR", e.strerror, sep="\n")

    while addr is None:

        user_input = input("----- Entrez une adresse IP CIDR : ----- \n")

        try:
            addr = IPAddress.from_str(user_input)
        except ValueError as e:
            print("\n> Erreur de syntaxe pour l'adresse IP CIDR", e.strerror, sep="\n> ")

    return addr

def load_answers():
    def convert_to_ip_info(dic_str):
        dic = json.loads(dic_str)
        return IPAddress.from_dict(dic)

    frontier_ans = list(map(convert_to_ip_info, open('data/frontiere.txt').readlines()))
    non_frontier_str = list(map(convert_to_ip_info, open('data/non-frontiere.txt').readlines()))

    return (frontier_ans, non_frontier_str)

# Un petit cadeau <3
def print_gj():
    print()
    print("░░█▀░░░░░░░░░░░▀▀███████░░░░░\n░░█▌░░░░░░░░░░░░░░░▀██████░░░\n░█▌░░░░░░░░░░░░░░░░███████▌░░\n░█░░░░░░░░░░░░░░░░░████████░░\n▐▌░░░░░░░░░░░░░░░░░▀██████▌░░\n░▌▄███▌░░░░▀████▄░░░░▀████▌░░\n▐▀▀▄█▄░▌░░░▄██▄▄▄▀░░░░████▄▄░\n▐░▀░░═▐░░░░░░══░░▀░░░░▐▀░▄▀▌▌\n▐░░░░░▌░░░░░░░░░░░░░░░▀░▀░░▌▌\n▐░░░▄▀░░░▀░▌░░░░░░░░░░░░▌█░▌▌\n░▌░░▀▀▄▄▀▀▄▌▌░░░░░░░░░░▐░▀▐▐░\n░▌░░▌░▄▄▄▄░░░▌░░░░░░░░▐░░▀▐░░\n░█░▐▄██████▄░▐░░░░░░░░█▀▄▄▀░░\n░▐░▌▌░░░░░░▀▀▄▐░░░░░░█▌░░░░░░\n░░█░░▄▀▀▀▀▄░▄═╝▄░░░▄▀░▌░░░░░░\n░░░▌▐░░░░░░▌░▀▀░░▄▀░░▐░░░░░░░\n░░░▀▄░░░░░░░░░▄▀▀░░░░█░░░░░░░\n░░░▄█▄▄▄▄▄▄▄▀▀░░░░░░░▌▌░░░░░░\n░░▄▀▌▀▌░░░░░░░░░░░░░▄▀▀▄░░░░░\n▄▀░░▌░▀▄░░░░░░░░░░▄▀░░▌░▀▄░░░\n░░░░▌█▄▄▀▄░░░░░░▄▀░░░░▌░░░▌▄▄\n░░░▄▐██████▄▄░▄▀░░▄▄▄▄▌░░░░▄░\n░░▄▌████████▄▄▄███████▌░░░░░▄\n░▄▀░██████████████████▌▀▄░░░░\n▀░░░█████▀▀░░░▀███████░░░▀▄░░\n░░░░▐█▀░░░▐░░░░░▀████▌░░░░▀▄░\n░░░░░░▌░░░▐░░░░▐░░▀▀█░░░░░░░▀\n░░░░░░▐░░░░▌░░░▐░░░░░▌░░░░░░░\n")
    print()

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
            ip_addr = IPAddress.from_str(format(ans, "m"))
            student_ans = ipcalc(ip_addr)
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
    ipcalc(addr)

if __name__ + "__main__":
    main()