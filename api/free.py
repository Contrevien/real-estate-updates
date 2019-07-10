import hmac
import hashlib
import binascii

key = "e179017a62b049968a38e91aa9f1"
message = "akkimysite@gmail.com"

key = binascii.unhexlify(key)
message = message.encode()

print(hmac.new(key, message, hashlib.sha256).hexdigest().lower())
