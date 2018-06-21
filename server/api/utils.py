titles = {
    # 1xx Informational
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    # 2xx Success
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    208: "Already Reported",
    226: "IM Used",
    # 3xx Redirection
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "Switch Proxy",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    # 4xx Client Error
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Time-out",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Payload Too Large",
    414: "URI Too Long",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",
    421: "Misdirected Request",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    451: "Unavailable For Legal Reasons",
    # 5xx Server Error
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Time-out",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    508: "Loop Detected",
    510: "Not Extended",
    511: "Network Authentication Required"
}


# MasonObject definition borrowed from Exercise 4
class MasonObject(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def __init__(self, **kwargs):
        super(MasonObject, self).__init__(**kwargs)
        if "@controls" not in self:
            self["@controls"] = {}

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.

        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.

        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.

        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md

        : param str ctrl_name: name of the control (including namespace if any)
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs

    def add_control_self(self, uri):
        self.add_control("self", href=uri)

    def add_control_create(self, uri, title, href, schema_url, method="POST", encoding="json"):
        self.add_control(uri, title=title, href=href, schema_url=schema_url, method=method, encoding=encoding)

    def add_control_edit(self, uri, title, href, schema_url, method="PATCH", encoding="json"):
        self.add_control(uri, title=title, href=href, schema_url=schema_url, method=method, encoding=encoding)

    def add_control_delete(self, uri, title, href):
        self.add_control(uri, title=title, href=href, method="DELETE")


class AccountId(MasonObject):
    def __init__(self, account_id, **kwargs):
        super(AccountId, self).__init__(**kwargs)
        self["account_id"] = account_id
        self["title"] = "Related account ID"
        self.add_control_self("/accounts/{}".format(account_id))


class CardSHA(MasonObject):
    def __init__(self, sha, **kwargs):
        super(CardSHA, self).__init__(**kwargs)
        self["card_sha"] = sha
        self["title"] = "Related card SHA"
        self.add_control_self("/cards/{}".format(sha))


class UserId(MasonObject):
    def __init__(self, user_id, **kwargs):
        super(UserId, self).__init__(**kwargs)
        self["user_id"] = user_id
        self["title"] = "Related user ID"
        self.add_control_self("/users/{}".format(user_id))


class RegisterSHA(MasonObject):
    def __init__(self, sha, **kwargs):
        super(RegisterSHA, self).__init__(**kwargs)
        self["register_sha"] = sha
        self["title"] = "Related register SHA"
        self.add_control_self("/registers/{}".format(sha))


def status(code, detail=""):
    return {
        "status": code,
        "title": titles[code],
        "detail": detail,
        "type": "about:blank"
    }, code
