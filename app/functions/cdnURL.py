from typing import Optional

def location_to_cdn(location: dict) ->  Optional[str]:
    """
    Turns location into CDN link
    :param location: file location data
    :return: file location
    """
    split = location["file_path"].split("/")
    if len(split) > 0:
        match split[0]:
            case "vleedn":
                return location["file_path"].replace("vleedn", "https://cdn.vlee.me.uk")
            case _:
                return None