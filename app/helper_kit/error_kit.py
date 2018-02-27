from flask import make_response, jsonify

from app import prepare_json_response


class ErrorKit:

    @staticmethod
    def return_error(e):
        error = ""
        if hasattr(e, 'args'):
            if len(e.args) > 0:
                error = e.args[0]
        else:
            error = "Error inserting answer"

        return make_response(
            jsonify(
                prepare_json_response(
                    message="Answered",
                    success=True,
                    total_pages=0,
                    total_itens=0,
                    current_page=1,
                    data={"message": error}
                )
            ), 400
        )