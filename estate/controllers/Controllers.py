from odoo import http

class MyController(http.Controller):
    @http.route(route='/reports', auth='public')
    def hellorUser(self):
        # userProperty= http.request.env['estate.property'].sudo().search(['|', ('salesperson', '=', http.request.env.user.id), ('salesperson', '=', False)])
        breakpoint()
        userProperty= http.request.env['estate.property'].sudo().search([])
        print(userProperty)
        return http.request.render("estate.estate_property_offer_template",{
            'docs': userProperty
        })