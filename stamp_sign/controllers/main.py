from odoo import http
from odoo.addons.sign.controllers.main import Sign


class SignController(Sign):
    def get_document_qweb_context(self, sign_request_id, token, **post):
        data = super().get_document_qweb_context(sign_request_id, token, **post)
        current_request_item = data["current_request_item"]
        sign_item_types = data["sign_item_types"]
        data["logo"] = (
            "data:image/png;base64,%s" % http.request.env.user.company_id.logo.decode()
        )

        if current_request_item:
            for item_type in sign_item_types:
                if item_type["item_type"] == "stamp":
                    user_stamp = current_request_item._get_user_stamp()
                    user_stamp_frame = current_request_item._get_user_stamp_frame()
                    item_type["auto_value"] = (
                        "data:image/png;base64,%s" % user_stamp.decode()
                        if user_stamp
                        else False
                    )
                    item_type["frame_value"] = (
                        "data:image/png;base64,%s" % user_stamp_frame.decode()
                        if user_stamp_frame
                        else False
                    )

        return data
