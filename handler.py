from domain.fx_service import FXService


def handler(event, context):
    # Determine which handler to use based on the event
    if event["path"] == "/cadusd-fx":
        fx_handler = FXService()
        return fx_handler.handle_request(event)
