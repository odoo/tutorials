from odoo import http
from odoo.http import request


class POSConfigInfo(http.Controller):

    @http.route("/pos/get_display_layout", type='json', auth='user')
    def get_display_layout(self,config_id=None):
        pos_config = request.env['pos.config'].browse(config_id)
        disp_layout = pos_config.pos_disp_type or 'default'

        return {'disp_layout': disp_layout}
