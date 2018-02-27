from app import app
from app.helper_kit.json_kit import JsonKit
from pyfcm import FCMNotification

from app.models.push import PushNotificationModel


class PushNotificationKit(object):
    push_service = FCMNotification(api_key=app.config['FCM_KEY'])
    package_name = "br.com.medt.medico"
    message_title = "MEDT"

    def __init__(self):
        pass

    @staticmethod
    def send(registration_ids,
             push_model: PushNotificationModel
             ):

        if len(registration_ids) > 0:
            result = PushNotificationKit.push_service.notify_multiple_devices(registration_ids=registration_ids,
                                                                              message_title=PushNotificationKit.message_title,
                                                                              message_body=push_model.message_body,
                                                                              click_action="FCM_PLUGIN_ACTIVITY",
                                                                              data_message=push_model.data_message
                                                                              )
            if len(result) > 0 and (isinstance(result, dict) or isinstance(result, list)):
                if len(result) > 0:
                    if "success" in result:
                        if result['success'] == 1:
                            return True

                    if "failure" in result:
                        if result['failure'] == 1:
                            return False
            else:
                return False