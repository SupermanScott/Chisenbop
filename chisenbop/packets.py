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
        now = time.time()
        keys = []
        for (granularity, count_of_keys) in configuration:
            key_value = Packet.determineTimeAgo(event_date, granularity)
            expire_timestamp = self.determineExpiration(granularity, count_of_keys)
            if expire_timestamp > now:
                key_string = "%s:%s:%s:%s" % (granularity, key_value, self.event, self.version,)
                keys.append((key_string, int(expire_timestamp),))
        return keys

    def determineExpiration(self, granularity, number_of_keys):
        """
        Determine when this event should expire
        """
        secs_year = 31556926

        if granularity == 'seconds':
            return self.timestamp + number_of_keys
        if granularity == 'minutes':
            exact = datetime.datetime.fromtimestamp(
                self.timestamp + 60 * number_of_keys)
            return time.mktime(
                datetime.datetime(exact.year, exact.month, exact.day,
                                  exact.hour, exact.minute).timetuple())
        if granularity == 'hours':
            exact = datetime.datetime.fromtimestamp(
                self.timestamp + 3600 * number_of_keys)
            return time.mktime(
                datetime.datetime(exact.year, exact.month, exact.day,
                                  exact.hour).timetuple())
        if granularity == 'days':
            return time.mktime(
                datetime.date.fromtimestamp(
                    self.timestamp + 86400 * number_of_keys).timetuple())
        if granularity == 'months':
            exact = datetime.date.fromtimestamp(
                self.timestamp  + 2629743 * number_of_keys)
            return time.mktime(
                datetime.date(exact.year, exact.month, 1).timetuple())
        if granularity == 'years':
            exact = datetime.date.fromtimestamp(
                self.timestamp + secs_year * number_of_keys)
            # Gets me 1/1/YEAR_OF_EXPIRATION
            return time.mktime(
                datetime.date(exact.year, 1, 1).timetuple())

    @classmethod
    def determineTimeAgo(cls, event_date, granularity):
        """
        Returns the integer for the event date in the given granularity
        """
        timestamp = int(time.mktime(event_date.timetuple()))
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
