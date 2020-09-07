import flask
import pygame

html_app = flask.Flask(__name__)

pygame.init()
screen = None
screen = pygame.display.set_mode(flags=(
    pygame.NOFRAME
    #| pygame.FULLSCREEN
))

background = pygame.image.load('images/earth-base/background.png').convert()
screen.blit(background, (0,0))

pygame.display.flip()
#pygame.display.update()
# Ignore events, but need to pass control to get display actually updated
print(pygame.event.get())

def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@html_app.route('/')
def control_sheet():
    pages=[
        { 'name': 'control',     'url': '/' },
        { 'name': 'exit-server', 'url': '/exit-server' },
    ]
    return flask.render_template('earth-base-control.html',
                                 pages=pages,
                                 ip=get_ip(),
                                 )

@html_app.route('/exit-server')
def exit_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'
