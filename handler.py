from domain.fx_service import FXService


def lambda_handler(event, context):
    # Determine which handler to use based on the event
    print(event, context)
    if event["path"] == "/cadusd-fx":
        fx_handler = FXService()
        return fx_handler.handle_request(event)
