from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class DentalPortal(CustomerPortal):
    @http.route('/my/dental', type='http', auth='user', website=True)
    def portal_my_dental(self, **kw):
        users = request.env.user.search([])
        return request.render('dental_application.portal_my_dental', {
            'users': users
        })

    @http.route('/my/dental/<int:user_id>', type='http', auth='user', website=True)
    def portal_my_dental_user(self, user_id, **kw):
        return request.render('dental_application.portal_my_dental_user')
