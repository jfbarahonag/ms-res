from app.config.variables import URL_MOTOR

class RequestService:
    @staticmethod
    def get_request(request_id: int):
        return URL_MOTOR
    
    @staticmethod
    def hello_world():
        return "Hello world"