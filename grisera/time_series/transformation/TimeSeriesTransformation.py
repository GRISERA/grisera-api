from typing import List, Optional

from grisera.property.property_model import PropertyIn
from grisera.time_series.time_series_model import TimeSeriesOut


class TimeSeriesTransformation:
    """
    Abstract class to handle logic of time series transformation

    """

    def transform(self, time_series: List[TimeSeriesOut], additional_properties: Optional[List[PropertyIn]]):
        """
        Transform time series data

        Args:
            time_series (List[TimeSeriesOut]): Time series to be transformed
            additional_properties (Optional[List[PropertyIn]]): Transformation parameters

        Returns:
            New time series object
        """
        raise Exception("transform not implemented yet")
