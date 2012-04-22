# -*- coding: utf-8 -*-
#
# © 2012 Scott Reynolds
# Author: Scott Reynolds <scott@scottreynolds.us>
#
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet import defer
from twisted.python import log
import txredisapi as redis
import sys

import chisenbop.packets as packets

class ChisenbopProtocol(DatagramProtocol):
    def __init__(self, configuration):
        self.config = configuration

    @defer.inlineCallbacks
    def datagramReceived(self, datagram, address):
        loaded_packet = packets.Packet(datagram)
        for (key, expires) in loaded_packet.constructKeys(self.config):
            conn = yield redis.Connection(reconnect=False)
            txn = yield conn.multi()
            txn.incr(key)
            txn.expire(key, expires)
            yield txn.commit()

def main():
    log.startLogging(sys.stdout)
    configuration = (
        ("seconds", 10,),
        ("minutes", 60,),
        ("hours", 24,),
        ("years", 4,),
        )
    reactor.listenUDP(8000, ChisenbopProtocol(configuration))
    reactor.run()

if __name__ == '__main__':
    main()
