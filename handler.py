from domain.fx_service import FXService


def lambda_handler(event, context):
    # Determine which handler to use based on the event
    if event["fc.request_uri"] == "/cadusd-fx":
        fx_handler = FXService()
        return fx_handler.process_fx_data()
