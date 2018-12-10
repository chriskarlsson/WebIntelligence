from django.core.exceptions import MiddlewareNotUsed

from assignment3.logic.data_store import get_data
from assignment3.logic.disk_to_database import load_data


class LoadData:
    def __init__(self, _):
        load_data()
        get_data()
        raise MiddlewareNotUsed
