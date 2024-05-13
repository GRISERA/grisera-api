from typing import List

from grisera.time_series.time_series_model import TimeSeriesOut, Type, TimeSeriesMultidimensionalOut
from grisera.time_series.ts_helpers import get_node_property


class TimeSeriesTransformationMultidimensional:
    """
    Class with logic of time series multidimensional transformation

    """

    def transform(self, time_series: List[TimeSeriesOut]):
        """
        Transform time series data.

        Get signal values lists grouped by timestamp values.
        This transformation will ignore all signal values which timestamps will not be equal.

        Args:
            time_series (List[TimeSeriesOut]): Time series to be transformed

        Returns:
            New time series object
        """
        assert len(time_series) > 0, "Number of time series should be at least 1 for multidimensional transformation"
        for i in range(1, len(time_series)):
            assert time_series[0].type == time_series[i].type, "Time series types should be equal"

        new_signal_values = []
        current_signal_value_rest_indexes = [0] * len(time_series)
        timestamp_label = "timestamp" if time_series[0].type == Type.timestamp else "start_timestamp"
        # Iterate over all X signal values
        for current_signal_value_x in time_series[0].signal_values:
            match = True
            signal_values = [current_signal_value_x["signal_value"]]
            for i in range(1, len(time_series)):
                # For current X signal value find first Y, Z and other signal values with greater or equal timestamp
                # value
                # If not found, return not existing indexes
                while current_signal_value_rest_indexes[i] < len(time_series[i].signal_values) and \
                        int(get_node_property(
                            time_series[i].signal_values[current_signal_value_rest_indexes[i]]["timestamp"],
                            timestamp_label)) < int(
                    get_node_property(current_signal_value_x["timestamp"], timestamp_label)):
                    current_signal_value_rest_indexes[i] += 1
                # Check if X, Y, Z and other signal timestamps are the same
                if current_signal_value_rest_indexes[i] < len(time_series[1].signal_values) and \
                        get_node_property(current_signal_value_x["timestamp"], "timestamp") == get_node_property(
                    time_series[i].signal_values[current_signal_value_rest_indexes[i]]["timestamp"], "timestamp") and \
                        get_node_property(current_signal_value_x["timestamp"], "start_timestamp") == get_node_property(
                    time_series[i].signal_values[current_signal_value_rest_indexes[i]]["timestamp"],
                    "start_timestamp") and \
                        get_node_property(current_signal_value_x["timestamp"], "end_timestamp") == get_node_property(
                    time_series[i].signal_values[current_signal_value_rest_indexes[i]]["timestamp"], "end_timestamp"):
                    signal_values.append(
                        time_series[i].signal_values[current_signal_value_rest_indexes[i]]["signal_value"])
                else:
                    match = False
                    break
            if match:
                new_signal_values.append({
                    "timestamp": current_signal_value_x["timestamp"],
                    "signal_values": signal_values
                })

        return TimeSeriesMultidimensionalOut(type=time_series[0].type, signal_values=new_signal_values)
