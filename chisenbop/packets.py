# -*- coding: utf-8 -*-
#
# © 2012 Scott Reynolds
# Author: Scott Reynolds <scott@scottreynolds.us>
#
import datetime
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
        keys = []
        for (granularity, count_of_keys) in configuration:
            todays_value = Packet.determineTimeAgo(now, granularity)
            key_value = Packet.determineTimeAgo(event_date, granularity)
            if todays_value - key_value < count_of_keys:
                keys.append("%s:%s:%s" % (key_value, self.event, self.version,))
        return keys

    @classmethod
    def determineTimeAgo(cls, event_date, granularity):
        """
        Returns the integer for the event date in the given granularity
        """
        if granularity == 'seconds':
            return event_date.second
        if granularity == 'minutes':
            return event_date.minute
        if granularity == 'hours':
            return event_date.hour
        if granularity == 'days':
            return event_date.day
        if granularity == 'months':
            return event_date.month
        if granularity == 'years':
            return event_date.year

        raise ValueError("Provided granularity is not supported")
