#!/usr/bin/python3.6
from functools import reduce

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

"""
    Classe pour representer la notation "decimal dot" (EX : 165.92.12.71)
        - Être affichee en format binaire           : format(ddn, "b")
        - Être affichee en format decimale          : str(ddn)
        - Donner le resultat du et logique          : ddn & autre_ddn
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

        def place_byte_in_value(byte_index):
            offset = byte_index * 8
            byte_mask = ~(-1 << 8) << offset
            return Byte((dec & byte_mask) >> offset)

        ddn.byte_groups = list(map(place_byte_in_value, reversed(range(4))))
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
        def place_byte(value, byte_info):
            byte_index, byte = byte_info
            offset_byte = int(byte) << ((3 - byte_index) * 8)
            return value | offset_byte

        return reduce(place_byte, enumerate(self.byte_groups), 0)

    def __str__(self):
        return ".".join(map(str, self.byte_groups))

    # Operateurs
    def __and__(self, other_ddn):
        def logical_and(byte_index):
            my_byte = self.byte_groups[byte_index]
            other_byte = other_ddn.byte_groups[byte_index]
            return my_byte & other_byte

        return DecimalDotNotation.from_byte_groups(list(map(logical_and, range(4))))

    def __invert__(self):
        mask = ~(-1 << 32)
        return DecimalDotNotation.from_dec(int(self) ^ mask)

    def __add__(self, addend):
        val = int(self)
        return DecimalDotNotation.from_dec(val + addend)

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
