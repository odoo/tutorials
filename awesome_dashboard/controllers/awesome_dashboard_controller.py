from odoo import http
from odoo.http import request

class AwesomeDashboardController(http.Controller):

    @http.route('/awesome_dashboard/save_settings', type='json', auth='user')
    def save_settings(self, new_disabled_items):
        current_user = http.request.env.user
        user_dashboard_settings = http.request.env['user.dashboard.settings'].sudo().search([('user_id', '=', current_user.id)], limit=1)
        disabled_items = ",".join(new_disabled_items)
        
        if user_dashboard_settings:
            user_dashboard_settings.write({'disabled_items': disabled_items})
        else:
            http.request.env['user.dashboard.settings'].sudo().create({
                'user_id': current_user.id,
                'disabled_items': disabled_items
            })
        return True

    @http.route('/awesome_dashboard/get_settings', type='json', auth='user')
    def get_settings(self):
        current_user = http.request.env.user
        user_dashboard_settings = http.request.env['user.dashboard.settings'].sudo().search([('user_id', '=', current_user.id)], limit=1)
        if user_dashboard_settings and user_dashboard_settings.disabled_items:
            return user_dashboard_settings.disabled_items.split(',')
        return []
