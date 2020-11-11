import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(status_code=404)
    else:
        loan_amount = req_body.get('loan_amount')
        total_amount = req_body.get('total_amount')

        # If the loan exceeds 75% of the ammount amount return 403
        # Else return 200.
        if(loan_amount > total_amount * 0.75):
            return func.HttpResponse(status_code=403)
        else:
            return func.HttpResponse(status_code=200)
