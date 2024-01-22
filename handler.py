import logging

from domain.fx_service import FXService

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def lambda_handler(environ, start_response):
    # Determine which handler to use based on the event
    request_uri = environ["fc.request_uri"]
    if request_uri == "/cadusd-fx":
        fx_handler = FXService()
        result = fx_handler.process_fx_data()
        logging.info(result)
        status = "200 OK"
        start_response(status)
        return [result]
    else:
        status = "404 NOT FOUND"
        start_response(status)
        return []
