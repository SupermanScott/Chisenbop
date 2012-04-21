# -*- coding: utf-8 -*-
#
# © 2012 Scott Reynolds
# Author: Scott Reynolds <scott@scottreynolds.us>
#
import chisenbop.packets as packets
import datetime
import nose.tools

def test_determineTimeAgoSeconds():
    """
    Test logic of time ago class method
    """
    now = datetime.datetime.now()
    assert packets.Packet.determineTimeAgo(now, "seconds") == now.second, \
        "Timeago failed to return the second when asked"
    assert packets.Packet.determineTimeAgo(now, "minutes") == now.minute, \
        "Timeago failed to return the minute when asked"
    assert packets.Packet.determineTimeAgo(now, "hours") == now.hour, \
        "Timeago failed to return the hours when asked"
    assert packets.Packet.determineTimeAgo(now, "days") == now.day, \
        "Timeago failed to return the day when asked"
    assert packets.Packet.determineTimeAgo(now, "months") == now.month, \
        "Timeago failed to return the month when asked"
    assert packets.Packet.determineTimeAgo(now, "years") == now.year, \
        "Timeago failed to return the year when asked"

@nose.tools.raises(ValueError)
def test_determineTimeAgoInvalid():
    now = datetime.datetime.now()
    packets.Packet.determineTimeAgo(now, "invalid_config")
