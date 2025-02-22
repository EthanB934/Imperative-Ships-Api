from enum import Enum
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler


class status(Enum):
    HTTP_200_SUCCESS = 200
    HTTP_201_SUCCESS_CREATED = 201
    HTTP_204_SUCCESS_NO_RESPONSE_BODY = 204
    HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA = 400
    HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND = 404
    HTTP_500_SERVER_ERROR = 500


class HandleRequests(BaseHTTPRequestHandler):

    def response(self, body, code):
        self.set_response_code(code)
        self.wfile.write(body.encode())

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split("/")
        resource = path_params[1]

        url_dictionary = {"requested_resource": resource, "query_params": {}, "pk": 0}

        if parsed_url.query:
            try:
                # The query property begins as a string.
                # The string includes a row name, and a value expected at that table
                query = parse_qs(parsed_url.query)
                # The parse_qs breaks the initial query into two pieces to from a dictionary
                # The key of that dictionary becomes the row name
                # The value of that dictionary becomes the expected value at that key
                url_dictionary["query_params"] = query
                query_list = query["pk"]
                url_dictionary["pk"] = int(query_list[0])
                # The dictionary becomes nested inside the url dictionary.
            except (KeyError):
                    print("Make sure to use pk in query")
        return url_dictionary

    def set_response_code(self, status):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()
