import os
import pty
import select
import sys

class Shell:
    def __init__(self, chan):
        self.chan = chan

    def cmdloop(self):
        pid, fd = pty.fork()
        if pid == 0:
            print('\033[1;32m--- ROOTKIT ---\033[0m')
            print('\033[1;31mHello')
            print('\033[1;0m', end='')
            penis = input("$ ")
            print('Your input:', penis)
            sys.exit()
        else:
            while True:
                # select is not the most efficient thing out there but
                # it surely is fine for now
                rlist, wlist, xlist = select.select([fd, self.chan], [], [])

                if fd in rlist:
                    try:
                        data = os.read(fd, 1024)
                    except:
                        break
                    if len(data) == 0:
                        break
                    self.chan.send(data)

                if self.chan in rlist:
                    if self.chan.recv_ready():
                        data = self.chan.recv(1024)
                        if len(data) == 0:
                            break
                        os.write(fd, data)
