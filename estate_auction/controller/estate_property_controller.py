from odoo import http
from odoo.http import request
from odoo.addons.estate.controller.main import EstatePropertyController


class EstatePropertyController(EstatePropertyController):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def property_list(self, page=1, property_sale_type=None, **kwargs):
        response = super().property_list(page=page, **kwargs)

        if property_sale_type:
            response.qcontext["properties"] = response.qcontext["properties"].filtered(lambda property: property.property_sale_type == property_sale_type)

        return response
