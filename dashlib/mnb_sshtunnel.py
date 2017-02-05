import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

    
import subprocess
import time
import threading
import signal

from config import *


class SshTunnel(threading.Thread):

    def __init__(
            self,
            localport,
            remoteport,
            remoteuser,
            remotehost,
            identityfile):
        threading.Thread.__init__(self)
        self.localport = localport      # Local port to listen to
        self.remoteport = remoteport    # Remote port on remotehost
        self.remoteuser = remoteuser    # Remote user on remotehost
        self.remotehost = remotehost    # What host do we send traffic to
        self.identityfile = identityfile
        self.daemon = True              # So that thread will exit when
        # main non-daemon thread finishes

    def run(self):
        if not USE_IDENTITYFILE:
            p = subprocess.Popen([
                'ssh', '-N',
                       '-L', str(self.localport) + ':localhost:' + str(self.remoteport),
                       self.remoteuser + '@' + self.remotehost])
        else:
            p = subprocess.Popen([
                'ssh', '-i', self.identityfile,
                       '-N',
                       '-L', str(self.localport) + ':localhost:' + str(self.remoteport),
                       self.remoteuser + '@' + self.remotehost])            

        if p:
            self.pid = p.pid

        else:
            raise Exception('ssh tunnel setup failed')

    def _getpid(self):
        return self.pid


def start_ssh_tunnel():
    tunnel = SshTunnel(
        SSH_LOCAL_PORT,
        rpcport,
        SSH_USER,
        SSH_SERVER,
        SSH_IDENTITYFILE)
    tunnel.start()
    time.sleep(1)

    return tunnel
