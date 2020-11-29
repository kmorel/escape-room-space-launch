import flask
import threading
import sys
import os
import traceback
import qr_response

import panda3d.core

html_app = flask.Flask(__name__)

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
        { 'name': 'control',         'url': '/' },
        { 'name': 'container entry', 'url': '/container-entry' },
        { 'name': 'containers',      'url': '/container' },
        { 'name': 'move 0-->1',      'url': '/move/0/1' },
        { 'name': 'move 0-->2',      'url': '/move/0/2' },
        { 'name': 'move 0<--1',      'url': '/move/1/0' },
        { 'name': 'move 1-->2',      'url': '/move/1/2' },
        { 'name': 'move 0<--2',      'url': '/move/2/0' },
        { 'name': 'move 1<--2',      'url': '/move/2/1' },
        { 'name': 'heli attack',     'url': '/heli' },
        #{ 'name': 'exit-server',     'url': '/exit-server' },
    ]
    return flask.render_template('control.html',
                                 pages=pages,
                                 name='Earth Base',
                                 ip=get_ip(),
                                 port=5000
                                 )

@html_app.route('/qr')
def qr_gen():
    data = flask.request.args.get('data')
    print('Generating QR code for ', data)
    return qr_response.generate(data)

# @html_app.route('/exit-server')
# def exit_server():
#     print('Shutting down server...')
#     func = flask.request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     print('  Calling flask shutdown')
#     func()
#     print('  Calling panda3d shutdown')
#     panda3d_base.userExit()
#     print('  Returning')
#     return 'Server shutting down...'

did_container_intro = False

@html_app.route('/container-entry')
def container_entry():
    global did_container_intro
    if not did_container_intro:
        return qr_response.generate('http://' + get_ip() + ':5000/container')
    else:
        return container_control()

@html_app.route('/container')
def container_control():
    global did_container_intro
    if not did_container_intro:
        did_container_intro = True
        global go_to_armory_sound
        go_to_armory_sound.play()
    return flask.render_template('earth-base-containers.html',
                                 m01=containers.can_move(0,1),
                                 m02=containers.can_move(0,2),
                                 m10=containers.can_move(1,0),
                                 m12=containers.can_move(1,2),
                                 m20=containers.can_move(2,0),
                                 m21=containers.can_move(2,1),
                                 )

@html_app.route('/move/<int:start>/<int:end>')
def move(start, end):
    containers.move(start, end)
    return container_control()

@html_app.route('/heli')
def do_heli():
    heli.attack()
    return flask.render_template('walkie-talkie.html')

def start(base, container_stacks, helicopter):
    global panda3d_base
    panda3d_base = base
    global containers
    containers = container_stacks
    global go_to_armory_sound
    go_to_armory_sound = base.loader.loadSfx('audio/dialogue/go-to-armory.ogg')
    global heli
    heli = helicopter
    # The graphics usually work better on the main thread, so make flask run
    # on a separate thread. (That we we can return right away, too.)
    threading.Thread(
        target=html_app.run,
        kwargs={
            'host': '0.0.0.0',
            #'port': 80,
        }).start()

def stop():
    # Hard exit (to quit out of the flask thread in case)
    os._exit(0)
