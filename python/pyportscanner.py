#!/usr/bin/env python
from socket import *

if __name__ == '__main__':
    target = raw_input('Enter host to scan: ')
    low = int(raw_input('Enter low port to scan:'))
    hi = int(raw_input('Enter high port to scan:'))
    targetIP = gethostbyname(target)
    print 'Starting scan on host ', targetIP

    #scan reserved ports
    for i in range(low, hi):
        print i
        s = socket(AF_INET, SOCK_STREAM)
        try:
            j = s.connect_ex((target, i))
            print i
            if(result == 0):
                try:
                    srv = getservbyport(i)
                except:
                    srv = ""
                print 'Port %d OPEN - %s' % (i, srv)
            j.close()
        except:
            pass
