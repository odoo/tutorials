from odoo.http import request, route 
from odoo import http


class EstateController(http.Controller):

    # ------------------------------------------------------------
    # PROPERTIES PAGE
    # ------------------------------------------------------------
    @route('/properties', auth='public', website=True)
    def get_properties(self, **kwargs):
        
        properties_data = request.env['estate.property'].sudo().search([]) 

        return request.render("estate.estate_web_properties", {
            "properties": properties_data
        })


    # ------------------------------------------------------------
    # SPECIFIC PROPERTY PAGE
    # ------------------------------------------------------------
    @route('/property/<int:property_id>', auth='public', website=True)
    def get_property(self, property_id, **kwargs):

        property_data = request.env['estate.property'].sudo().browse(property_id)

        if not property_data:
            return request.not_found()

        return request.render("estate.estate_web_property_details", {
            "property": property_data
        })

