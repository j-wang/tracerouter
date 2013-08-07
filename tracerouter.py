"""
File: tracerouter.py
Author: James Wang
Date: 6 Aug 2013
License: MIT

Simple traceroute server, primarily written for educational purposes.

"""
# TODOs: Debug strange timeout issues
#        Async traces with non-blocking sockets
#        Send multiple packets per ttl loop

import socket


def trace(dest, PORTNUM=5005, max_hops=30):
    """Traceroute to specified hostname (e.g. 'google.com'). Can optionally
    specify port to send on (defaults 5005).

    """
    IPADDR = socket.gethostbyname(dest)

    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')

    ack = False
    ttl = 1

    print "Starting trace to {0}, {1}".format(dest, IPADDR)

    while not ack:
        curr_addr, curr_name = None, None

        # Initialize and connect UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        r = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        s.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        r.bind(("", PORTNUM))
        s.sendto("", (IPADDR, PORTNUM))

        try:
            r.settimeout(3)  # don't block forever
            dat, curr_addr = r.recvfrom(512)

            # curr_addr is in form (host, port)
            try:
                curr_name = socket.gethostbyaddr(curr_addr[0])[0]
            except socket.error:
                curr_name = curr_addr[0]

        # Catch timeout errors
        except socket.error:
            pass
        finally:
            s.close()
            r.close()

        if curr_addr is None:
            curr_host = "*"
        else:
            curr_host = "{0} ({1})".format(curr_name, curr_addr[0])
            if curr_addr[0] == IPADDR or ttl > max_hops:
                ack = True

        print "{0}\t{1}".format(ttl, curr_host)

        ttl += 1


def main():
    dest = 'google.com'
    trace(dest)


if __name__ == '__main__':
    main()
