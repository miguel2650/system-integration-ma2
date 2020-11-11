import logging
import json

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(status_code=404)
    else:
        amount = req_body.get('amount')
        # Amount + 2% of the amount
        calculation = int(amount) * 1.02

        return func.HttpResponse(json.dumps({"amount": calculation}), mimetype="application/json")
