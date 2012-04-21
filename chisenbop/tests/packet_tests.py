# -*- coding: utf-8 -*-
#
# © 2012 Scott Reynolds
# Author: Scott Reynolds <scott@scottreynolds.us>
#
import chisenbop.packets as packets
import datetime
import time
import nose.tools

def test_determineTimeAgoSeconds():
    """
    Test logic of time ago class method
    """
    now = datetime.datetime.now()
    timestamp = int(time.mktime(now.timetuple()))
    assert packets.Packet.determineTimeAgo(now, "seconds") == timestamp, \
        "Timeago failed to return the second when asked"
    assert packets.Packet.determineTimeAgo(now, "minutes") == timestamp / 60, \
        "Timeago failed to return the minute when asked"
    assert packets.Packet.determineTimeAgo(now, "hours") == timestamp / 3600, \
        "Timeago failed to return the hours when asked"
    assert packets.Packet.determineTimeAgo(now, "days") == timestamp / 86400, \
        "Timeago failed to return the day when asked"
    assert packets.Packet.determineTimeAgo(now, "months") == timestamp / 2629743, \
        "Timeago failed to return the month when asked"
    assert packets.Packet.determineTimeAgo(now, "years") == timestamp / 31556926, \
        "Timeago failed to return the year when asked"

@nose.tools.raises(ValueError)
def test_determineTimeAgoInvalid():
    now = datetime.datetime.now()
    packets.Packet.determineTimeAgo(now, "invalid_config")

def test_keyConstruction():
    current_time = time.time()
    event_name = "test"
    version = "1.0"
    configuration = (
        ("seconds", 1,),
        ("minutes", 60 * 24 * 30,),
        )

    packet = packets.Packet("%s!%s!%s" % 
                            (current_time, event_name, version,))
    keys = packet.constructKeys(configuration)
    assert len(keys) == 2, \
        "Two keys were not returned: %s" % keys
    time.sleep(1)
    packet = packets.Packet("%s!%s!%s" % 
                            (current_time, event_name, version,))
    keys = packet.constructKeys(configuration)
    assert len(keys) == 1, \
        "Failed to prevent writing for the additional key: %s" % keys
