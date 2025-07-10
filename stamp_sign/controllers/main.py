from odoo import http
from odoo.addons.sign.controllers.main import Sign


class Sign(Sign):
    def get_document_qweb_context(self, sign_request_id, token, **post):
        data = super().get_document_qweb_context(sign_request_id, token, **post)
        current_request_item = data["current_request_item"]
        sign_item_types = data["sign_item_types"]
        company_logo = http.request.env.user.company_id.logo
        if company_logo:
            data["logo"] = "data:image/png;base64,%s" % company_logo.decode()
        else:
            data["logo"] = False

        if current_request_item:
            user_stamp = current_request_item._get_user_signature_asset("stamp_sign_stamp")
            user_stamp_frame = current_request_item._get_user_signature_asset("stamp_sign_stamp_frame")

            encoded_user_stamp = (
                "data:image/png;base64,%s" % user_stamp.decode()
                if user_stamp
                else False
            )
            encoded_user_stamp_frame = (
                "data:image/png;base64,%s" % user_stamp_frame.decode()
                if user_stamp_frame
                else False
            )

            stamp_item_type = next(
                (
                    item_type
                    for item_type in sign_item_types
                    if item_type["item_type"] == "stamp"
                ),
                None,
            )

            if stamp_item_type:
                stamp_item_type["auto_value"] = encoded_user_stamp
                stamp_item_type["frame_value"] = encoded_user_stamp_frame

        return data

    @http.route(["/sign/update_user_signature"], type="json", auth="user")
    def update_signature(
        self, sign_request_id, role, signature_type=None, datas=None, frame_datas=None
    ):
        user = http.request.env.user
        if not user or signature_type not in [
            "sign_signature",
            "sign_initials",
            "stamp_sign_stamp",
        ]:
            return False

        sign_request_item_sudo = (
            http.request.env["sign.request.item"]
            .sudo()
            .search(
                [("sign_request_id", "=", sign_request_id), ("role_id", "=", role)],
                limit=1,
            )
        )

        allowed = sign_request_item_sudo.partner_id.id == user.partner_id.id
        if not allowed:
            return False
        user[signature_type] = datas[datas.find(",") + 1 :]
        if frame_datas:
            user[signature_type + "_frame"] = frame_datas[frame_datas.find(",") + 1 :]
        return True
