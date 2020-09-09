#!/usr/bin/env python3

import flask
import pygame
import threading
import sys
import os
import traceback

import earth_base_shipping_container

FPS = 30

html_app = flask.Flask(__name__)

pygame.init()

screen = pygame.display.set_mode(flags=(
    pygame.FULLSCREEN |
    0
))

sprites = pygame.sprite.Group()

clock = pygame.time.Clock()
running = True

background = pygame.image.load('images/earth-base/background.png').convert()
screen.blit(background, (0,0))

containers = earth_base_shipping_container.ContainerStacks(sprites)
containers.move(0, 1)

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
    try:
        # pygame really wants to run on the main thread, so make flask run
        # on a separate thread
        threading.Thread(
            target=html_app.run,
            kwargs={
                'host': '0.0.0.0',
                'port': 80,
            }).start()

        print('Starting graphics event loop.')
        pygame.display.flip()
        while running:
            clock.tick(FPS)

            #screen.blit(background, test_container.rect, test_container.rect)
            for sprite in sprites:
                rect = sprite.rect
                screen.blit(background, rect, rect)
                pygame.display.update(rect)

            sprites.update()

            sprites.draw(screen)
            for sprite in sprites:
                rect = sprite.rect
                pygame.display.update(rect)

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif (event.type == pygame.KEYDOWN) and (event.key == ord('q')):
                    running = False

        print(clock.get_fps())

        print('Stopping graphics event loop.')
        pygame.quit()

    except:
        traceback.print_exc(file=sys.stdout)

    finally:
        # Hard exit (to quit out of the flask thread in case)
        os._exit(0)
