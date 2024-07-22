from odoo.http import route, Controller, request


class PropertyController(Controller):

    @route('/properties', auth='public', website='True')
    def handlePropertyPortal(self):
        values = {
            "properties": request.env['estate.property'].search([])
        }
        return request.render('estate.portal_estate_property_list', values)

    @route("/property/<model('estate.property'):prop>", auth='public', website='True')
    def handlePropertyDetailPortal(self, prop):
        values = {
            "property": prop
        }
        return request.render('estate.portal_estate_property_detail', values)
