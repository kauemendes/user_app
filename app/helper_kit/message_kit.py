from app.helper_kit.email_kit import EmailKit
from app.helper_kit.push_notification_kit import PushNotificationKit, PushNotificationModel
from app.models.emails import EmailModel


class MessageKit:
    _push_notification = None
    _emailkit = None

    @staticmethod
    def dispatcher(email_to_send: object = None,
                   email_type: EmailModel = None,
                   user_registration_id: list = None,
                   push_notification_type: PushNotificationModel = None

                   ):
        """
        :param email_to_send:
        :param email_type:
        :param user_registration_id:
        :param push_notification_type:
        :return:
        """

        if isinstance(email_to_send, str):
            email_to_send = [email_to_send]

        if isinstance(user_registration_id, str):
            user_registration_id = [user_registration_id]

        MessageKit._push_notification = PushNotificationKit()
        MessageKit._emailkit = EmailKit()

        lOk = True

        if email_to_send and email_type:
            try:
                lOk = MessageKit._emailkit.message_dispatch(email_to_send, email_type._TEMPLATE_SUBJECT_, email_type._TEMPLATE_RENDER_)
            except Exception as e:
                return False

        if lOk and push_notification_type and user_registration_id:
            try:
                lOK = MessageKit._push_notification.send(user_registration_id, push_notification_type)
            except Exception as e:
                return False

        return lOk
