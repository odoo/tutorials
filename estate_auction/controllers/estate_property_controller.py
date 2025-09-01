from odoo import http
from odoo.addons.estate.controllers.main import EstatePropertyController


class EstateControllerExtended(EstatePropertyController):
    @http.route(["/properties", "/properties/page/<int:page>"], type="http", auth="public", website=True)
    def property_list(self, page=1, **kwargs):
        response = super().property_list(page, **kwargs)

        sale_mode = kwargs.get("sale_mode")
        if sale_mode in ["auction", "regular"]:
            response.qcontext["properties"] = response.qcontext["properties"].filtered(lambda property: property.sale_mode == sale_mode)
        
        return response
