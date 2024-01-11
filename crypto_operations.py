import secrets
from ecpy.curves import Point, Curve
import random
import hashlib

def generate_keypair(curve: Curve):
    e1 = curve.generator
    d = int.from_bytes(secrets.token_bytes(16), 'big')
    e2 = d * e1
    pubKey = e2
    privKey = d
    return pubKey, privKey

def message_to_point(curve: Curve, message: bytes) -> Point:
    coordinate_size = curve.size // 8
    min_padding_size = 2
    max_message_size = coordinate_size - min_padding_size

    if len(message) > max_message_size:
        raise ValueError('Message too long')

    padding_size = coordinate_size - len(message)
    padded_message = bytearray(message) + b'\0' * padding_size
    padded_message[len(message)] = 0xff

    while True:
        x = int.from_bytes(padded_message, 'little')
        y = curve.y_recover(x)
        if y is None:
            padded_message[-1] += 1
        else:
            return Point(x, y, curve)
        
def point_to_message(point, curve):
    coordinate_size = curve.size // 8
    padded_message = point.x.to_bytes(coordinate_size, 'little')
    message_size = padded_message.rfind(0xff)
    message = padded_message[:message_size]
    return message

def encrypt(public_key: Point, message: bytes, curve: Curve) -> bytes:
    message_point = message_to_point(curve, message)
    r = random.randrange(0, curve.field)
    c1 = r * curve.generator
    c2 = r * public_key + message_point

    encrypted = bytes(curve.encode_point(c1) + curve.encode_point(c2))

    return encrypted

def decrypt(curve: Curve, secret_key: int, ciphertext: bytes) -> bytes:
    c1_bytes = ciphertext[:len(ciphertext) // 2]
    c2_bytes = ciphertext[len(ciphertext) // 2:]
    c1 = curve.decode_point(c1_bytes)
    c2 = curve.decode_point(c2_bytes)

    message_point = c2 - secret_key * c1
    decrypted = point_to_message(message_point, curve)

    return decrypted


def calculate_md5(data):
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    return md5_hash.digest()
