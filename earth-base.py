#!/usr/bin/env python3

import flask
import pygame
import threading

FPS = 30

html_app = flask.Flask(__name__)

pygame.init()
screen = None
screen = pygame.display.set_mode(flags=(
    pygame.NOFRAME
    #| pygame.FULLSCREEN
))

clock = pygame.time.Clock()
running = True

background = pygame.image.load('images/earth-base/background.png').convert()

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
    global running
    running = False
    return 'Server shutting down...'

if __name__ == '__main__':
    # pygame really wants to run on the main thread, so make flask run
    # on a separate thread
    threading.Thread(
        target=html_app.run,
        kwargs={
            'port': 80,
            'host': '0.0.0.0',
        }).start()

    print('Starting graphics event loop.')
    while running:
        clock.tick(FPS)

        screen.blit(background, (0,0))
        pygame.display.flip()
        # Ignore events (use web server instead)
        pygame.event.get()

    print('Stopping graphics event loop.')
