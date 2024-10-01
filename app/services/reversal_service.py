from app.schemas.request_schema import RequestMaintenanceSchema 

class RequestReversalService:
    @staticmethod
    def handle_reversal_request(reversal: RequestMaintenanceSchema):
        return reversal.advisor.email