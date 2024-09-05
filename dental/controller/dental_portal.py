from odoo import http
from odoo.http import request


class DentalPortal(http.Controller):

    @http.route(['/my/dental'], type='http', auth="user", website=True)
    def portal_my_dental(self, **kw):
        user = request.env.user
        DentalPatient = request.env['dental.patient']
        patients = DentalPatient.search([('guarantor_id', '=', user.partner_id.id)])

        values = {
            'patients': patients,
        }
        return request.render("dental.portal_my_dental", values)
