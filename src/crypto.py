""" Cryptographic primitives. """

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA


def get_hasher():
    """ Returns a object that you can use for hashing. Currently SHA512, swap it out for something if you feel like it! """
    return SHA512.new()

MAX_HASH = (1 << 512) - 1

class Signing:
    def __init__(self, byte_repr):
        self.rsa = RSA.importKey(byte_repr)

    def verify_sign(self, hashed_value, signature):
        """ Verify a signature for a already hashed value and a public key. """
        ver = PKCS1_v1_5.new(self.rsa)
        h = get_hasher()
        h.update(hashed_value)
        return ver.verify(h, signature)

    def sign(self, hashed_value):
        """ Sign a hashed value with a private key. """
        signer = PKCS1_v1_5.new(self.rsa)
        h = get_hasher()
        h.update(hashed_value)
        return signer.sign(h)

    @classmethod
    def generatePrivateKey(cls):
        return Signing(RSA.generate(3072).exportKey())

    def as_bytes(self, include_priv=False):
        """ bytes representation of this key. """
        if include_priv:
            return self.rsa.exportKey()
        else:
            return self.rsa.publickey().exportKey()
