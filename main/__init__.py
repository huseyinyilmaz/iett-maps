import cherrypy

class Root:
    def index(self):
        # Ask for the user's name.
#        import ipdb; ipdb.set_trace()

        return cherrypy.templates.get_template('index.html').render()
    index.exposed = True
