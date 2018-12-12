from django.core.exceptions import MiddlewareNotUsed

from assignment3.logic.data_store import get_data


class LoadData:
    def __init__(self, _):
        get_data()
        print('Data loaded')
        raise MiddlewareNotUsed
