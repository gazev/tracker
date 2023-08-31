from webob import Request

import os
import database
import hashlib
import shelve
import urllib.parse
import bencode

DB_PATH = './resource/things.db'

def create_dirs():
    dirname = os.path.dirname(DB_PATH)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


class Tracker:
    def __call__(self, environ, start_response):
        req = Request(environ)

        if req.method != 'GET':
            start_response(HTTP_400_BAD_REQUEST, [CONTENT_HEADER])
            return [HTTP_400_MESSAGE]

        if req.path_info != '/announce':
            start_response(HTTP_404_NOT_FOUND, [CONTENT_HEADER])
            return [HTTP_404_MESSAGE]

        params = query_to_map(environ['QUERY_STRING'])

        info_hash  = get_value(params, 'info_hash',  lambda x: urllib.parse.unquote_to_bytes(x).hex())
        peer_id    = get_value(params, 'client_id',  None)
        port       = get_value(params, 'port',       int)
        compact    = get_value(params, 'compact',    int)
        event      = get_value(params, 'event',      None)
        numwant    = get_value(params, 'numwant',    int)

        if not info_hash:
            start_response(HTTP_200_OK, [CONTENT_HEADER])
            return self.build_fail_response(fail_reason=MISSING_INFO_HASH)
        if not peer_id:
            start_response(HTTP_200_OK, [CONTENT_HEADER])
            return self.build_fail_response(fail_reason=MISSING_PEER_ID)
        if not port:
            start_response(HTTP_200_OK, [CONTENT_HEADER])
            return self.build_fail_response(fail_reason=MISSING_PORT)
        if not event:
            start_response(HTTP_200_OK, [CONTENT_HEADER])
            return self.build_fail_response(fail_reason=MISSING_EVENT)

        if not self.has_torrent(info_hash):
            start_response(HTTP_404_NOT_FOUND, [CONTENT_HEADER])
            return [HTTP_404_MESSAGE]

        ip = get_client_addr(environ)

        # add this peer to the db    
        with database.get_db() as db:
            db[info_hash][ip] = (port, event)

        return [b'Good\n']
    
    def has_torrent(self, info_hash: str) -> bool:
        with database.get_db() as db:
            return info_hash in db
    
    def build_fail_response(self, fail_reason: str):
        return [bencode.dumps({"failure reason": fail_reason})]    

    def build_response(
        self,
        info_hash: str, 
        numwant:   int, 
        interval:  int,
        *,
        warn:      str = "",
    ):

        peers_list = get_peers(info_hash, numwant)    

        response = {
            "interval":   interval,
            "complete":   get_nr_of_complete_peers(),
            "incomplete": get_nr_of_incomplete_peers(),
            "peers":      [pass]
        }

        if warn:
            response["warning message"] = message
        
        return [bencode.dumps(response)]


create_dirs()
tracker = Tracker()

