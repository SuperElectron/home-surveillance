import pymongo

from typing import Dict
from pymongo.collection import Collection



class BaseRepository:
    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    def _add_sorting(self, sort_params: Dict[str, str]) -> Dict[str, any]:
        query = []
        
        for sort_key, sort_value in sort_params.items():
            if sort_value == "asc":
                query.append((sort_key, pymongo.ASCENDING))
            else: 
                query.append((sort_key, pymongo.DESCENDING))

        return query

    def _add_filters(self) -> None: 
        raise NotImplemented