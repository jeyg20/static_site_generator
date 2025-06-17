from livereload import Server, shell

server = Server()
server.watch("docs/style.css")
server.watch("docs/index.html")
server.serve(port=5500, host="0.0.0.0", root="docs/")
