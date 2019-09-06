#!/usr/bin/python3.6
from functools import reduce

# Classe pour le correcteur
class IPInfo:
    def __init__(self, ip_addr, mask, wildcard, network, broadcast, hostmin, hostmax, hosts):
        self.ip_addr = format(ip_addr, "m") if isinstance(ip_addr, IPAddress) else ip_addr
        self.mask = str(mask)
        self.wildcard = str(wildcard)
        self.network = str(network) if network is not None else None
        self.broadcast = str(broadcast) if broadcast is not None else None
        self.hostmin = str(hostmin) if hostmin is not None else None
        self.hostmax = str(hostmax) if hostmax is not None else None
        self.hosts = str(hosts)

    @staticmethod
    def from_dict(dic):
        ip_addr = dic["Address"]
        mask = dic["Netmask"]
        wildcard = dic["Wildcard"]
        network =  dic["Network"] if "Network" in dic else None
        broadcast = dic["Broadcast"] if "Broadcast" in dic else None
        hostmin = dic["HostMin"] if "HostMin" in dic else None
        hostmax = dic["HostMax"] if "HostMax" in dic else None
        hosts = dic["Hosts/Net"]
        return IPInfo(ip_addr, mask, wildcard, network, broadcast, hostmin, hostmax, hosts)

    def __eq__(self, ip_info):
        equal = True

        def print_error(val_name, ans, student_ans):
            print("{0} incorrect pour l'adresse {1} : {2} devrait être {3}".format(val_name, ip_info.ip_addr, student_ans, ans))
            print()

        if self.wildcard is not None and self.wildcard != ip_info.wildcard:
            print_error("Wildcard", self.wildcard, ip_info.wildcard)
            equal = False

        if self.network is not None and self.network != ip_info.network:
            print_error("Adresse de réseau", self.network, ip_info.network)
            equal = False

        if self.broadcast is not None and self.broadcast != ip_info.broadcast:
            print_error("Adresse de broadcast", self.broadcast, ip_info.broadcast)
            equal = False

        if self.hostmin is not None and self.hostmin != ip_info.hostmin:
            print_error("Première adresse disponible", self.hostmin, ip_info.hostmin)
            equal = False

        if self.hostmax is not None and self.hostmax != ip_info.hostmax:
            print_error("Dernière adresse disponible", self.hostmax, ip_info.hostmax)
            equal = False

        if self.hosts is not None and self.hosts != ip_info.hosts:
            print_error("Nombre d'hôte", self.hosts, ip_info.hosts)
            equal = False

        return equal

def gen_mask(length):
    """
        Cree un bitmask rempli de 1 de longeur n (la taille de notre masque)
        Demonstration avec une longeur de 8 bits:
          > 1                  = 0000 0000 0001
          > 1 << 8 = 256       = 0001 0000 0000
                                      <<<<8<<<<
          > (1 << 8) - 1 = 255 = 0000 1111 1111
    """
    mask = (1 << length) - 1

    """
        Decale le masque de (32 - n) bits vers la gauche pour le positionner a la bonne place
          > 255               = 0000 0000 0000 0000 0000 0000 1111 1111
          > 255 << (32 - 8)
          > 255 << 26         = 1111 1111 0000 0000 0000 0000 0000 0000
                                          <<<<<<<<<<<26<<<<<<<<<<<<<<<<
    """
    return DecimalDotNotation.from_dec(mask << (32 - length))

"""
    Classe pour representer un Octet. Elle peut :
        - Être affichee en format binaire    : format(octet, "b")
        - Être affichee en format decimale   : str(octet)
        - Donner le resultat du "et" logique : octet & autre octet

    Cet objet est cree de la facon suivante : Byte(valeur_decimale)
"""
class Byte:
    def __init__(self, value):
        if not isinstance(value, int):
            raise ValueError
        self.value = value

    # Affichage
    def __format__(self, fmt):
        if "b" in fmt:
            byte = format(self.value, "08b")
            return "{0} {1}".format(byte[:4], byte[4:])

        return str(self)

    def __repr__(self):
        return "Byte({0})".format(str(self))

    # Casting
    def __str__(self):
        return str(self.value)

    def __int__(self):
        return self.value

    # Operateur
    def __and__(self, other_byte):
        return Byte(int(self) & int(other_byte))

    def __or__(self, other_byte):
        return Byte(int(self) | int(other_byte))

"""
    Classe pour representer la notation "decimal dot" (EX : 165.92.12.71)
        - Être affichee en format binaire           : format(ddn, "b")
        - Être affichee en format decimale          : str(ddn)
        - Donner le resultat du et logique          : ddn & autre_ddn
        - Donner le resultat du ou logique          : ddn | autre_ddn
        - Donner le resultat d'une addition         : ddn + autre_ddn
        - Donner le resultat de la negation binaire : ~ddn

    Cet objet peut être cree de trois facons :
        - DecimalDotNotation()
        - DecimalDotNotation.from_dec(valeur_decimale)
        - DecimalDotNotation.from_byte_group(liste_d_octets)
"""
class DecimalDotNotation:
    def __init__(self):
        self.byte_groups = []

    @staticmethod
    def from_dec(dec):
        ddn = DecimalDotNotation()
        """
            Decompose une valeur 32 bits en 4 octets a partir d'un index
            Exemple :
            4 294 963 200 = 1111 1111 1111 1111 1111 0000 0000 0000
            Index d'octet   └---3---┘ └---2---┘ └---1---┘ └---0---┘
                                |         |         |         |
                               255   .   255   .   240   .    0
        """
        def extract_byte_at_index(byte_index):
            offset = byte_index * 8

            # On cree un bitmask d'octet et on le place au bon decalage
            byte_mask = (1 << 8) - 1 << offset

            """
                On fait un et logique pour avoir la bonne valeur et remet la valeur
                au bon positionnement :
                  1111 1111 1111 1111 1111 0000 0000 0000
                ^ 0000 0000 0000 0000 1111 1111 0000 0000
                  =======================================
                  0000 0000 0000 0000 1111 0000 0000 0000
                Index d'octet         ├---1---┘         |
                1 * 8 = 8             └------61440------┘
                  0000 0000 0000 0000 0000 0000 1111 0000
                  >>>>8>>>>                     └--240--┘
            """
            return Byte((dec & byte_mask) >> offset)
        """
            On doit inverser nos index, pour la raison suivante :
            Index dans un tableau :   0    1    2   3
                                    [255, 255, 240, 0]
            Index dans 32 bits    :   3    2    1   0
        """
        ddn.byte_groups = list(map(extract_byte_at_index, reversed(range(4))))
        return ddn

    @staticmethod
    def from_byte_groups(byte_groups):
        ddn = DecimalDotNotation()
        ddn.byte_groups = byte_groups
        return ddn

    # Affichage
    def __format__(self, fmt):
        if "b" in fmt:
            return " . ".join(list(map(lambda b: format(b, "b"), self.byte_groups)))
        return str(self)

    def __repr__(self):
        return "DecimalDotNotation({0})".format(str(self))

    # Casting
    def __int__(self):

        # L'action inverse de "extract_byte_at_index"
        def place_byte_at_index(value, byte_info):

            # Prend notre valeur de bit : 240 = 1111 0000
            byte_index, byte = byte_info

            """
                On la deplace vers le bon index : 1 * 8 = 8
                value         = 0000 0000 0000 0000 0000 0000 0000 0000
                byte          = 0000 0000 0000 0000 0000 0000 1111 0000
                                                            └--240--┘
                offset_byte   = 0000 0000 0000 0000 1111 0000 0000 0000
                                <<<<8<<<<           └------61440------┘
                ou logique -> V 0000 0000 0000 0000 0000 0000 0000 0000 (valeur de value)
                                =======================================
                return        = 0000 0000 0000 0000 1111 0000 0000 0000

                La valeur de retour sera conserve et reutilise pour la prochaine iteration
                elle deviendra eventuellement notre valeur 32 bits.
            """
            offset_byte = int(byte) << (byte_index * 8)
            return value | offset_byte

        return reduce(place_byte_at_index, enumerate(reversed(self.byte_groups)), 0)

    def __str__(self):
        return ".".join(map(str, self.byte_groups))

    # Operateurs
    def __and__(self, other_ddn):

        # Le "et" logique est tout simplement un "et" entre chancun
        # des 4 octets de nos 32 bits
        def logical_and(byte_index):
            my_byte = self.byte_groups[byte_index]
            other_byte = other_ddn.byte_groups[byte_index]
            return my_byte & other_byte

        return DecimalDotNotation.from_byte_groups(list(map(logical_and, range(4))))

    def __or__(self, other_ddn):

        # Meme chose que le "et" logique
        def logical_or(byte_index):
            my_byte = self.byte_groups[byte_index]
            other_byte = other_ddn.byte_groups[byte_index]
            return my_byte | other_byte

        return DecimalDotNotation.from_byte_groups(list(map(logical_or, range(4))))

    # Pour inverser les 32 bits j'utilise ce que l'on appel un "ou exclusif" (xor)
    # couple avec un bitmask de 32 bits à 1.
    def __invert__(self):
        mask = (1 << 32) - 1
        """
            mask   = 1111 1111 1111 1111 1111 1111 1111 1111
            valeur = 1111 1111 1111 1111 1111 0000 0000 0000
                 xor =======================================
                     0000 0000 0000 0000 0000 1111 1111 1111
        """
        return DecimalDotNotation.from_dec(int(self) ^ mask)
    """
        Pour faire l'adition je converti d'abbord mon objet DecimalDotNotation
        en int et je fait l'addition de celle-ci. Je retourne ensuite un objet
        DecimalDotNotation contenant la somme de l'addtion.
    """
    def __add__(self, addend):
        val = int(self)
        return DecimalDotNotation.from_dec(val + int(addend))

    # La soustraction est comme le "et" logique.
    def __sub__(self, subtrahend):
        val = int(self)
        return DecimalDotNotation.from_dec(val - int(subtrahend))

"""
    Classe pour representer une adresse IP CIDR
        - Être affichee en format binaire  : format(adresse, "b")
        - Être affichee en format decimale : str(adresse)
        - Être affichee en format CIDR     : format(adresse, "m")

    Cet objet est cree de la facon suivante : IPAddress(ddn, longeur_du_masque)
"""
class IPAddress:
    def __init__(self, ddn, mask_length):
        self.ddn = ddn
        self.mask_length = mask_length

    # Affichage
    def __format__(self, fmt):
        output = str(self)

        if "b" in fmt:
            output = format(self.ddn, "b")

        if "m" in fmt:
            output += "/{0}".format(self.mask_length)

        return output

    def __repr__(self):
        return "IPAddress(ddn={0}, mask_length={1})".format(self.ddn, self.mask_length)

    # Casting
    def __str__(self):
        return str(self.ddn)

# Un petit cadeau <3
def print_gj():
    print()
    print("░░█▀░░░░░░░░░░░▀▀███████░░░░░\n░░█▌░░░░░░░░░░░░░░░▀██████░░░\n░█▌░░░░░░░░░░░░░░░░███████▌░░\n░█░░░░░░░░░░░░░░░░░████████░░\n▐▌░░░░░░░░░░░░░░░░░▀██████▌░░\n░▌▄███▌░░░░▀████▄░░░░▀████▌░░\n▐▀▀▄█▄░▌░░░▄██▄▄▄▀░░░░████▄▄░\n▐░▀░░═▐░░░░░░══░░▀░░░░▐▀░▄▀▌▌\n▐░░░░░▌░░░░░░░░░░░░░░░▀░▀░░▌▌\n▐░░░▄▀░░░▀░▌░░░░░░░░░░░░▌█░▌▌\n░▌░░▀▀▄▄▀▀▄▌▌░░░░░░░░░░▐░▀▐▐░\n░▌░░▌░▄▄▄▄░░░▌░░░░░░░░▐░░▀▐░░\n░█░▐▄██████▄░▐░░░░░░░░█▀▄▄▀░░\n░▐░▌▌░░░░░░▀▀▄▐░░░░░░█▌░░░░░░\n░░█░░▄▀▀▀▀▄░▄═╝▄░░░▄▀░▌░░░░░░\n░░░▌▐░░░░░░▌░▀▀░░▄▀░░▐░░░░░░░\n░░░▀▄░░░░░░░░░▄▀▀░░░░█░░░░░░░\n░░░▄█▄▄▄▄▄▄▄▀▀░░░░░░░▌▌░░░░░░\n░░▄▀▌▀▌░░░░░░░░░░░░░▄▀▀▄░░░░░\n▄▀░░▌░▀▄░░░░░░░░░░▄▀░░▌░▀▄░░░\n░░░░▌█▄▄▀▄░░░░░░▄▀░░░░▌░░░▌▄▄\n░░░▄▐██████▄▄░▄▀░░▄▄▄▄▌░░░░▄░\n░░▄▌████████▄▄▄███████▌░░░░░▄\n░▄▀░██████████████████▌▀▄░░░░\n▀░░░█████▀▀░░░▀███████░░░▀▄░░\n░░░░▐█▀░░░▐░░░░░▀████▌░░░░▀▄░\n░░░░░░▌░░░▐░░░░▐░░▀▀█░░░░░░░▀\n░░░░░░▐░░░░▌░░░▐░░░░░▌░░░░░░░\n")
    print()