from odoo import http
from odoo.addons.sign.controllers.main import Sign
import logging
_logger = logging.getLogger(__name__)


class Sign(Sign):
    def get_document_qweb_context(self, sign_request_id, token, **post):
        result = super().get_document_qweb_context(sign_request_id, token, **post)
        context = result.get('rendering_context', {})
        current_request_item = context.get('current_request_item')
        sign_item_types = context.get('sign_item_types')
        company_logo = http.request.env.user.company_id.logo
        if company_logo:
            context['logo'] = "data:image/png;base64,%s" % company_logo.decode()
        else:
            context['logo'] = False
        if current_request_item and sign_item_types:
            user_stamp = current_request_item._get_user_stamp('stamp_sign_stamp')
            user_stamp_frame = current_request_item._get_user_stamp_frame('stamp_sign_stamp_frame')
            encoded_stamp = ("data:image/png;base64,%s" % user_stamp.decode() if user_stamp else False)
            encoded_frame = ("data:image/png;base64,%s" % user_stamp_frame.decode() if user_stamp_frame else False)
            for item_type in sign_item_types:
                if item_type.get('item_type') == 'stamp':
                    item_type['auto_value'] = encoded_stamp
                    item_type['frame_value'] = encoded_frame
                    break
        result['rendering_context'] = context
        return result

    @http.route(["/sign/update_user_signature"], type="jsonrpc", auth="user")
    def update_signature(self, sign_request_id, role, signature_type=None, datas=None, frame_datas=None):
        if signature_type == "stamp_sign":
            signature_type = "stamp_sign_stamp"
        user = http.request.env.user
        if not user:
            return False
        if signature_type not in ['sign_signature', 'sign_initials', 'stamp_sign_stamp']:
            return False
        user[signature_type] = datas[datas.find(',') + 1:]
        user[signature_type + '_frame'] = frame_datas[frame_datas.find(',') + 1:] if frame_datas else False
        return True
