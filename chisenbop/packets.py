# -*- coding: utf-8 -*-
#
# © 2012 Scott Reynolds
# Author: Scott Reynolds <scott@scottreynolds.us>
#
import datetime
import time

class Packet(object):
    """
    Packet class represents the data that came in down the stream. It breaks the
    data into timestamp, event string and version.
    """
    def __new__(cls, encoded_data, *args, **kwargs):
        implementation = super(Packet, cls).__new__(cls, *args, **kwargs)
        implementation.timestamp = float(encoded_data.split("!")[0])
        implementation.event = encoded_data.split("!")[1]
        implementation.version = encoded_data.split("!")[2]

        return implementation

    def constructKeys(self, configuration):
        """
        Returns all the keys for the packet based on the configuration
        """
        event_date = datetime.datetime.fromtimestamp(self.timestamp)
        now = datetime.datetime.now()
        current_timestamp = time.mktime(now.timetuple())
        delta = now - event_date

        keys = []
        for (granularity, count_of_keys) in configuration:
            todays_value = Packet.determineTimeAgo(now, granularity)
            key_value = Packet.determineTimeAgo(event_date, granularity)
            if todays_value - key_value < count_of_keys:
                key_string = "%s:%s:%s" % (key_value, self.event, self.version,)
                expire_timestamp = current_timestamp - delta.microseconds / 100
                keys.append((key_string, expire_timestamp,))
        return keys

    @classmethod
    def determineTimeAgo(cls, event_date, granularity):
        """
        Returns the integer for the event date in the given granularity
        """
        timestamp = time.mktime(event_date.timetuple())
        if granularity == 'seconds':
            return timestamp
        if granularity == 'minutes':
            return timestamp / 60
        if granularity == 'hours':
            return timestamp / 3600
        if granularity == 'days':
            return timestamp / 86400
        if granularity == 'months':
            return timestamp / 2629743
        if granularity == 'years':
            return timestamp / 31556926

        raise ValueError("Provided granularity is not supported")
