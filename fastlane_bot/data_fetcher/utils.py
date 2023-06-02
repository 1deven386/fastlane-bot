from typing import Any, Union, Dict, List, Tuple, Set
from web3.datastructures import AttributeDict
from hexbytes import HexBytes
from typing import List

from fastlane_bot.data_fetcher.manager import Manager


def filter_latest_events(mgr: Manager, events: List[List[AttributeDict]]) -> List[AttributeDict]:
    """
    This function filters out the latest events for each pool. Given a nested list of events, it iterates through all events
    and keeps track of the latest event (i.e., with the highest block number) for each pool. The key used to identify each pool
    is derived from the event data using manager's methods.

    Args:
        mgr (Manager): A Manager object that provides methods to handle events and their related pools.
        events (List[List[AttributeDict]]): A nested list of events, where each event is an AttributeDict that includes
        the event data and associated metadata.

    Returns:
        List[AttributeDict]: A list of events, each representing the latest event for its corresponding pool.
    """
    latest_entry_per_pool = {}
    all_events = [event for event_list in events for event in event_list]
    for event in all_events:
        # print()
        # print(event)
        # print()
        key = mgr.pool_type_from_exchange_name(mgr.exchange_name_from_event(event)).unique_key()
        if key == 'cid':
            key = 'id'
        elif key == 'tkn1_address':
            if event["args"]["pool"] != mgr.cfg.BNT_ADDRESS:
                key = 'pool'
            else:
                key = 'tkn_address'
        unique_key = event[key] if key in event else event["args"][key]
        if unique_key not in latest_entry_per_pool:
            latest_entry_per_pool[unique_key] = event
        elif event["blockNumber"] > latest_entry_per_pool[unique_key]["blockNumber"]:
            latest_entry_per_pool[unique_key] = event

    return list(latest_entry_per_pool.values())


def complex_handler(obj: Any) -> Union[Dict, str, List, Set, Any]:
    """
    This function aims to handle complex data types, such as web3.py's AttributeDict, HexBytes, and native Python collections
    like dict, list, tuple, and set. It recursively traverses these collections and converts their elements into more "primitive"
    types, making it easier to work with these elements or serialize the data into JSON.

    Args:
        obj (Any): The object to be processed. This can be of any data type, but the function specifically handles AttributeDict,
        HexBytes, dict, list, tuple, and set.

    Returns:
        Union[Dict, str, List, Set, Any]: Returns a "simplified" version of the input object, where AttributeDict is converted
        into dict, HexBytes into str, and set into list. For dict, list, and tuple, it recursively processes their elements.
        If the input object does not match any of the specified types, it is returned as is.
    """
    if isinstance(obj, AttributeDict):
        return dict(obj)
    elif isinstance(obj, HexBytes):
        return obj.hex()
    elif isinstance(obj, bytes):
        return obj.hex()
    elif isinstance(obj, dict):
        return {k: complex_handler(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [complex_handler(i) for i in obj]
    elif isinstance(obj, set):
        return list(obj)
    else:
        return obj
