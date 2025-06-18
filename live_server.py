from livereload import Server

server = Server()
server.watch("docs/index.html")
server.watch("docs/style.css")
server.serve(port=5500, host="0.0.0.0", root="docs/")
