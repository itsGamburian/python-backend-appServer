# Hambartzum Gamburian
# Websocket & HTTP Requests

from tornado import websocket, web, ioloop
import json

c_l = []


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("../javascript-backend-radarWebApp/index.html")


class RadarGraphHandler(web.RequestHandler):
    def get(self):
        self.render("../javascript-backend-radarWebApp/radar.html")


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in c_l:
            c_l.append(self)

    def on_close(self):
        if self in c_l:
            c_l.remove(self)


class ApiHandler(web.RequestHandler):

    @web.asynchronous
    def get(self, *args):
        self.finish()
        id = self.get_argument("id")
        value = self.get_argument("value")
        data = {"id": id, "value" : value}
        data = json.dumps(data)
        for c in c_l:
            c.write_message(data)

    @web.asynchronous
    def post(self):
        pass


app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/api', ApiHandler),
    (r'/(radar.html)', web.StaticFileHandler, {'path': './'}),
    (r'/(socket.io)', web.StaticFileHandler, {'path': './'}),
    (r'/(sketch.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()