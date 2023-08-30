import hashlib
import bencode
import urllib.parse

def info_hash(info: dict) -> bytes:
    return urllib.parse.quote(hashlib.sha1(bencode.dumps(info)).hexdigest())
