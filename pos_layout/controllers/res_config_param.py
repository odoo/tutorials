from odoo import http
from odoo.http import request


class POSConfigInfo(http.Controller):

    @http.route("/pos/get_display_layout", type='json', auth='user')
    def get_display_layout(self):
        user_id = request.env.user.id
        pos_session = request.env['pos.session'].sudo().search([
            ('user_id', '=', user_id)
        ], limit=1)

        if not pos_session:
            return {'error': 'No POS session found for the user.'}

        pos_config = pos_session.config_id
        disp_layout = pos_config.pos_disp_type or 'default'
        all_pos_configs = request.env['pos.config'].sudo().search([])
        all_pos_configs.write({'pos_disp_type': disp_layout})
        all_pos_configs.write({'pos_disp_type': disp_layout})
        return {'disp_layout': disp_layout}
