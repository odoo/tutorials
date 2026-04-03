from odoo import http
from odoo.http import request


class DashboardController(http.Controller):

    @http.route('/awesome_dashboard/save_config', type='jsonrpc', auth='user')
    def save_config(self, config):
        request.env.user.sudo().dashboard_config = config
        return True

    @http.route('/awesome_dashboard/get_config', type='jsonrpc', auth='user')
    def get_config(self):
        return request.env.user.sudo().dashboard_config or "[]"
