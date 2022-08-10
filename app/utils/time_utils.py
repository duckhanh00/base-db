import datetime
import time
class TimeUtils:
    @staticmethod
    def round_timestamp(timestamp, round_time=86400):
        timestamp_unit_day = timestamp / round_time
        recover_to_unit_second = int(timestamp_unit_day) * round_time
        return recover_to_unit_second

    @staticmethod
    def get_values_by_frequency(change_logs, start_time=0, round_time=3600, min_value=False):
        results = {}
        last_timestamp = 0
        for t, v in change_logs.items():
            if t > start_time:
                if TimeUtils.round_timestamp(t, round_time) != TimeUtils.round_timestamp(last_timestamp, round_time):
                    results[t] = v
                    last_timestamp = t
                elif min_value and (v < results[last_timestamp]):
                    results.pop(last_timestamp)
                    results[t] = v
                    last_timestamp = t

        return results

    @staticmethod
    def format_timestamp(timestamp, format_="%m-%d-%Y, %H:%M:%S"):
        t = datetime.datetime.fromtimestamp(int(timestamp))
        return t.strftime(format_)

    @staticmethod
    def date_to_timestamp(date, _format="%d/%m/%Y"):
        return time.mktime(datetime.datetime.strptime(date, _format).timetuple())

    @staticmethod
    def get_value_with_timestamp(change_logs, timestamp_chosen, time_limit=None, sort=False):
        if sort:
            change_logs = sorted(change_logs.items(), key=lambda x: x[0])
        for idx, (timestamp, value) in enumerate(change_logs):
            if timestamp > timestamp_chosen:
                return value
            if time_limit and timestamp > timestamp_chosen + time_limit:
                break
        return None
