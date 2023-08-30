from utils import *
from webob import Request

import hashlib
import shelve
import urllib.parse


class Tracker:
    def __call__(self, environ, start_response):
        req = Request(environ)

        if req.method != "GET":
            start_response(HTTP_400_BAD_REQUEST, [CONTENT_HEADER])
            return [HTTP_400_MESSAGE]

        if req.path_info != "/announce":
            start_response(HTTP_404_NOT_FOUND, [CONTENT_HEADER])
            return [HTTP_404_MESSAGE]

        params = query_to_map(environ["QUERY_STRING"])

        info_hash  = get_value(params, "info_hash",  lambda x: urllib.parse.unquote_to_bytes(x).hex())
        peer_id    = get_value(params, "peer_id",    None)
        port       = get_value(params, "port",       int)
        uploaded   = get_value(params, "uploaded",   int)
        downloaded = get_value(params, "downloaded", int)
        left       = get_value(params, "left",       int)
        compact    = get_value(params, "compact",    int)

        if not self.has_torrent(info_hash):
            start_response(HTTP_404_NOT_FOUND, [CONTENT_HEADER])
            return [HTTP_404_NOT_FOUND]

        return [b"Good\n"]
    
    def has_torrent(self, info_hash: str):
        return True


class Database:
    __shared_state = {}

    def __init__(self):
        self.__db = __shared_state


tracker = Tracker()

