import cherrypy


class Root:
    def index(self):
        return cherrypy.templates.get_template('index.html').render()
    index.exposed = True
