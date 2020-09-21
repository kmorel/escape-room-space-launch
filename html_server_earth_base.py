import flask
import threading
import sys
import os
import traceback

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
        { 'name': 'control',     'url': '/' },
        #{ 'name': 'exit-server', 'url': '/exit-server' },
        { 'name': 'containers',  'url': '/container' },
        { 'name': 'move 0-->1',  'url': '/move/0/1' },
        { 'name': 'move 0-->2',  'url': '/move/0/2' },
        { 'name': 'move 0<--1',  'url': '/move/1/0' },
        { 'name': 'move 1-->2',  'url': '/move/1/2' },
        { 'name': 'move 0<--2',  'url': '/move/2/0' },
        { 'name': 'move 1<--2',  'url': '/move/2/1' },
    ]
    return flask.render_template('earth-base-control.html',
                                 pages=pages,
                                 ip=get_ip(),
                                 port=5000
                                 )

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

@html_app.route('/container')
def container_control():
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

def start(base, container_stacks):
    global panda3d_base
    panda3d_base = base
    global containers
    containers = container_stacks
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
