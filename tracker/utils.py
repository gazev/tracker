CONTENT_HEADER = ("Content-type", "text/plain")

HTTP_400_BAD_REQUEST = "400 Bad request"
HTTP_404_NOT_FOUND   = "404 Not found"

HTTP_400_MESSAGE = b"Bad request!"
HTTP_404_MESSAGE = b"File not found!"

def query_to_map(query: str):
    """ Returns a dictionary mapping all keys and values from a query string

    :param query: A URL encoded query string
    :return: A dictionary mapping all keys and values of given ``query``
    """
    query_pairs = query.split("&")

    # Dictionary comprehension for each pair in list of "a=b" type strings we split
    # and make the zero index item our key and the one index item our value 
    return {
        tup[0]:tup[1] \
            for tup in (pair_str.split("=") for pair_str in query_pairs)
    }


def get_value(map: dict, key: str, conv_func: callable = None, *args):
    """ Retrieve the value of given key from query parameters

    :param map: A dictionary-like object that maps the query parameters keys and values
    :param key: The desired key
    :param conv_func: A callable that will convert the retrieved string key to the
        desired data type, defaults to None (simply return a string) 
    :parm *args: Extra parameters used in ``conv_func`` call
    :return: The desired value or None if the key doesn't exist
    :rtype: Return type of ``conv_func`` 
    """
    if key not in map:
        return None
        
    if not conv_func:
        return map[key]

    if args:
        value =  conv_func(map[key], *args)
    else:
        value = conv_func(map[key])
    
    return value


