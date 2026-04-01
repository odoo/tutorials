from odoo.http import Controller, route, request


class EstateProperty(Controller):
    @route(['/properties'], type='http', auth='public', website=True)
    def properties(self):
        all_properties = request.env['estate.property'].search([])
        return request.render("estate.estateproperties", {'properties': all_properties})
