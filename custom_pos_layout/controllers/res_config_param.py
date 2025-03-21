from odoo import models,fields
from odoo import http  
from odoo.http import request

class POSConfigInfo(http.Controller):

    @http.route("/pos/get_display_layout",type='json',auth='user')
    def get_display_layout(self):
        user_id = request.env.user.id
        pos_session  = request.env['pos.session'].sudo().search([
            ('user_id', '=' , user_id)
        ],limit=1)
        pos_config = request.env['pos.config'].search([('id','=',pos_session.config_id.id)])
        disp_layout = pos_config.pos_disp_type
        print("IN CONTROLLER ===>>>===<<<===")
        print(disp_layout)
        return {'disp_layout': disp_layout}
