# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.addons.sign.controllers.main import Sign # type: ignore


class Sign(Sign):
    def get_document_qweb_context(self, sign_request_id, token, **post):
        data = super().get_document_qweb_context(sign_request_id, token, **post)
        company_logo = http.request.env.user.company_id.logo
        if company_logo:
            data["logo"] = "data:image/png;base64,%s" % company_logo.decode()
        else:
            data["logo"] = False

        return data

    @http.route(["/sign/update_user_signature"], type="json", auth="user")
    def update_signature(
        self, sign_request_id, role, signature_type=None, datas=None, frame_datas=None
    ):
        user = http.request.env.user
        if not user or signature_type not in [
            "sign_signature",
            "sign_initials",
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
        if datas:
            user[signature_type] = datas[datas.find(",") + 1 :]
        else:
            user[signature_type] = False

        if frame_datas:
            user[signature_type + "_frame"] = frame_datas[frame_datas.find(",") + 1 :]
        else:
            user[signature_type + "_frame"] = False

        return True
