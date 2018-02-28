

class ResponseReturnKit(object):

    @staticmethod
    def error400(msg="Failed to complete your request"):
        return {"error": msg}, 400
