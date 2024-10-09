from typing import Union, Optional

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.requests import Request

from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory
from grisera.time_series.time_series_model import (
    TimeSeriesIn,
    TimeSeriesNodesOut,
    TimeSeriesOut,
    TimeSeriesPropertyIn,
    TimeSeriesRelationIn,
    TimeSeriesTransformationIn,
    TimeSeriesMultidimensionalOut
)

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class TimeSeriesRouter:
    """
    Class for routing time series based requests

    Attributes:
        time_series_service (TimeSeriesService): Service instance for time series
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.time_series_service = service_factory.get_time_series_service()

    @router.post("/time_series", tags=["time series"], response_model=TimeSeriesOut)
    async def create_time_series(self, time_series: TimeSeriesIn, response: Response, dataset_id: Union[int, str]):
        """
        Create time series in database

        Signal values:
        - should be provided in ascending order of (start) timestamp
        - timestamps within one time series should be unique (for Timestamp type) and disjoint (for Epoch type)
        """

        create_response = self.time_series_service.save_time_series(time_series, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.post("/time_series/transformation", tags=["time series"],
                 response_model=Union[TimeSeriesOut, NotFoundByIdModel])
    async def transform_time_series(self, time_series_transformation: TimeSeriesTransformationIn, response: Response,
                                    dataset_id: Union[int, str]):
        """
        Create new transformed time series in database

        Each transformation uses a different set of parameters.

        Supported transformation names and parameters:
        - resample_nearest:
            - period (required) - difference between output timestamps
            - start_timestamp - first output timestamp (default 0)
            - end_timestamp - last output timestamp will be less than end_timestamp (default last input end timestamp + period)
        - quadrants:
            - origin_x - X value of the center point of coordinate system (default 0)
            - origin_y - Y value of the center point of coordinate system (default 0)

        To read about the implementation details go to TimeSeriesTransformation docstring documentation.
        """

        create_response = self.time_series_service.transform_time_series(time_series_transformation, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/time_series", tags=["time series"], response_model=TimeSeriesNodesOut)
    async def get_time_series_nodes(self, response: Response, dataset_id: Union[int, str], request: Request,
                                    entityname_property_name: Optional[str] = None,
                                    experiment_id: Union[int, str] = None,
                                    participant_id: Union[int, str] = None,
                                    participant_date_of_birth: Optional[str] = None,
                                    participant_sex: Optional[str] = None,
                                    participant_name: Optional[str] = None,
                                    participantstate_age: Optional[str] = None,
                                    recording_id: Union[int, str] = None,
                                    recording_source: Optional[str] = None):
        """
        Get time series from database.

        The list of available parameters is not limited to the given below.

        This request allows filtering time series by id or any property from entities connected to time series.
        The format of this generic GET filter parameter is: `entityname_property_name`.

        Supported entity names:
        - observableinformation
        - recording
        - participation
        - participantstate
        - participant
        - activityexecution
        - activity
        - experiment
        - registeredchannel
        - channel
        - registereddata
        """

        get_response = self.time_series_service.get_time_series_nodes(dataset_id, request.query_params)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/time_series/{time_series_id}",
        tags=["time series"],
        response_model=Union[TimeSeriesOut, NotFoundByIdModel],
    )
    async def get_time_series(
            self, time_series_id: Union[int, str], depth: int, response: Response, dataset_id: Union[int, str],
            signal_min_value: Optional[int] = None,
            signal_max_value: Optional[int] = None
    ):
        """
        Get time series by id from database with signal values. Depth attribute specifies how many models will be traversed to create the
        response.

        Signal values will be filtered using minimum and maximum value if present.
        """

        get_response = self.time_series_service.get_time_series(time_series_id, dataset_id, depth, signal_min_value,
                                                                signal_max_value)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/time_series/multidimensional/{time_series_ids}", tags=["time series"],
                response_model=Union[TimeSeriesMultidimensionalOut, NotFoundByIdModel])
    async def get_time_series_multidimensional(self, time_series_ids: str, response: Response, dataset_id: Union[int, str]):
        """
        Get multidimensional time series by ids from database with signal values.

        Time series ids is comma separated string.
        """
        try:
            ids = [int(time_series_id.strip()) for time_series_id in time_series_ids.split(",")]
        except ValueError:
            response.status_code = 422
            return TimeSeriesMultidimensionalOut(errors="Ids must be integers")

        get_response = self.time_series_service.get_time_series_multidimensional(ids, dataset_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/time_series/{time_series_id}",
        tags=["time series"],
        response_model=Union[TimeSeriesOut, NotFoundByIdModel],
    )
    async def delete_time_series(
            self, time_series_id: Union[int, str], response: Response, dataset_id
    ):
        """
        Delete time series by id from database with all signal values.
        """
        get_response = self.time_series_service.delete_time_series(time_series_id, dataset_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/time_series/{time_series_id}",
        tags=["time series"],
        response_model=Union[TimeSeriesOut, NotFoundByIdModel],
    )
    async def update_time_series(
            self,
            time_series_id: Union[int, str],
            time_series: TimeSeriesPropertyIn,
            response: Response, dataset_id: Union[int, str]
    ):
        """
        Update time series model in database
        """
        update_response = self.time_series_service.update_time_series(
            time_series_id, time_series, dataset_id
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.put(
        "/time_series/{time_series_id}/relationships",
        tags=["time series"],
        response_model=Union[TimeSeriesOut, NotFoundByIdModel],
    )
    async def update_time_series_relationships(
            self,
            time_series_id: Union[int, str],
            time_series: TimeSeriesRelationIn,
            response: Response, dataset_id: Union[int, str]
    ):
        """
        Update time series relations in database
        """
        update_response = self.time_series_service.update_time_series_relationships(
            time_series_id, time_series, dataset_id
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
