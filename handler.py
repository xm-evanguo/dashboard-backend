from domain.fx_service import FXHandler


def lambda_handler(event, context):
    # Determine which handler to use based on the event
    if event["path"] == "/cadusd-fx":
        fx_handler = FXHandler()
        return fx_handler.handle_request(event)
