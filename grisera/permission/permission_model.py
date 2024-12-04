from typing import Union, Optional, List

from grisera import BaseModelOut, DatasetIn


# TODO: DOCS

class BasicDatasetOut(DatasetIn):
    datasetId: Optional[Union[int, str]]
    userId: Optional[Union[int, str]]
    role: str


class PermissionsOut(BaseModelOut):
    permissions: Optional[List[BasicDatasetOut]]
