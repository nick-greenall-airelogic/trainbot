from nredarwin.webservice import DarwinLdbSession
import os

_DARWIN_SESH = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx",
                                api_key=os.environ['train_api'])


def board_for_shortcode(destination_shortcode, origin_shortcode="LDS"):
    board = _DARWIN_SESH.get_station_board(origin_shortcode, destination_crs=destination_shortcode)
    departures = []
    for service in board.train_services:
        time = str(service.etd) if service.etd != 'On time' else str(service.std)
        delayed = str(service.etd) if ':' not in service.etd else 'Delayed'
        departures.append(
            (str(service.destination_text), str(service.platform), delayed, time)
        )
    return departures
