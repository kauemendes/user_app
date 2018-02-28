from app.user import view


class StartApi:

    api_version = 'v1'

    def __init__(self, api, api_version=None):

        if api_version:
            self.api_version = api_version

        # Adiciona os endpoints aqui
        api.add_resource(view.UserResource, '/v1/user')
