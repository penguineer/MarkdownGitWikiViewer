#!/usr/bin/python3

import tornado.ioloop
import tornado.web
import tornado.netutil

import webbrowser

import argparse
import os



def load_asset(asset):
    progpath = os.path.dirname(os.path.realpath(__file__))
    
    f = open(progpath+"/assets/"+asset, "r")
    asset = f.read()
    f.close()
    
    return asset


class AssetHandler(tornado.web.RequestHandler):
    def get(self):
        path = self.request.uri[len("/assets/"):]
        
        if path.endswith(".html"):
            self.set_header("Content-Type", "text/html")
        elif path.endswith(".css"):
            self.set_header("Content-Type", "text/css")
        elif path.endswith(".js"):
            self.set_header("Content-Type", "text/javascript")
        else:
            self.set_header("Content-Type", "text/plain")
        
        self.write(load_asset(path))


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(load_asset("index.html"))


class DataHandler(tornado.web.RequestHandler):
    def get(self):
        global PATH_PREFIX
        path = PATH_PREFIX + self.request.uri[len("/data"):]
        
        try:
            f = open(path, "r")
            
            self.write(f.read())
            
            f.close()
            
        except FileNotFoundError:
            self.clear()
            self.set_status(404)
            self.finish("<html><body>File {0} cannot be found!</body></html>".format(path))


class StructureHandler(tornado.web.RequestHandler):
    def get(self):
        global PATH_PREFIX
        
        self.set_header("Content-Type", "text/html")
        
        self.write("<ul>\n")
        
        for root, dirs, files in os.walk(PATH_PREFIX):
            for f in files:
                if f.endswith(".md"):
                    href = os.path.join(root, f)[len(PATH_PREFIX):]
                    link = "<a href=\"javascript:switch_page('{0}')\">{0}</a>".format(href)
                    self.write("<li>")
                    self.write(link)
                    self.write("</li>\n")
        
        self.write("</ul>\n")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/wiki/.*", MainHandler),
        (r"/assets/.*", AssetHandler),
        (r"/data/.*", DataHandler),
        (r"/structure", StructureHandler)
    ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Show Markdown files as Wiki")
    parser.add_argument("--data", help="Data directory",
                        default=os.getcwd())
    args = parser.parse_args()
    
    global PATH_PREFIX
    PATH_PREFIX = args.data
    
    print("Data directory is {0}".format(PATH_PREFIX))
    
    app = make_app()
    sockets = tornado.netutil.bind_sockets(0, '')
    server = tornado.httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    
    port = None
    
    for s in sockets:
        print('Listening on %s, port %d' % s.getsockname()[:2])
        if port is None:
            port = s.getsockname()[1]
    
    webbrowser.open("http://localhost:{0}/".format(port))
    
    tornado.ioloop.IOLoop.current().start()


# kate: space-indent on; indent-width 4; mixedindent off; indent-mode python; indend-pasted-text false; remove-trailing-space off
