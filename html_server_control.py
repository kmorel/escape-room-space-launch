import flask
import threading
import sys
import os
import traceback
import qr_response

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
        { 'name': 'control',          'url': '/' },
        { 'name': 'button',           'url': '/self-destruct-button' },
        { 'name': 'do self destruct', 'url': '/do-self-destruct' },
        #{ 'name': 'exit-server',      'url': '/exit-server' },
    ]
    return flask.render_template('control.html',
                                 pages=pages,
                                 name='Control Panel',
                                 ip=get_ip(),
                                 port=5000
                                 )

@html_app.route('/self-destruct-button')
def self_destruct_button():
    return flask.render_template('self-destruct-button.html')

@html_app.route('/do-self-destruct')
def do_self_destruct():
    global self_destruct
    self_destruct.doDestruct()
    return flask.render_template('walkie-talkie.html')

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

def start(base, destruct):
    global panda3d_base
    panda3d_base = base
    global self_destruct
    self_destruct = destruct
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
