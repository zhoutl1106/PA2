from BaseHTTPServer import BaseHTTPRequestHandler
import logging
import urlparse
from process import process

class GetHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        x = self.wfile.write
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        parsed_path = urlparse.urlparse(self.path)
        word = parsed_path.query[5:]

        # <--- HTML starts here --->
        x("<html>")
        # <--- HEAD starts here --->
        x("<head><style>table, th, td {    border: 1px solid black;}</style>")
        x("<title>PA2</title>")
        x("</head>")
        # <--- HEAD ends here --->
        # <--- BODY starts here --->
        x("<body>")
        if len(word) > 0:
            x(process(word))
        else:
            x("<h1>Please input query text ( and/or/not & word group are support )</h1>")
            x('<form action="/server.py" method=GET>')
            x('<input type="text" name="word"><br/>')
            x('<input type="submit" value="Submit" />')

        x("</body>")
        # <--- BODY ends here --->
        x("</html>")
        # <--- HTML ends here --->
    # def do_POST(self):
    #     logging.warning("======= POST STARTED =======")
    #     logging.warning(self.headers)
    #     form = cgi.FieldStorage(
    #         fp=self.rfile,
    #         headers=self.headers,
    #         environ={'REQUEST_METHOD':'POST',
    #                  'CONTENT_TYPE':self.headers['Content-Type'],
    #                  })
    #     logging.warning("======= POST VALUES =======")
    #     for item in form.list:
    #         logging.warning(item)
    #     logging.warning("\n")
    #     SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', 8080), GetHandler)
    print 'Starting server, use <Ctrl + F2> to stop'
    server.serve_forever()
