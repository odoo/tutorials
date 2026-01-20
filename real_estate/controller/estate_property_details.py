from odoo import http
from odoo.http import request


class EstateDetails(http.Controller):
    @http.route(["/property/<int:property_id>"], website=True, auth="public")
    def current_property(self, property_id, **kw):
        property = request.env["estate.property"].sudo().browse(property_id)

        if not property.exists():
            return request.not_found()

        return request.render(
            "real_estate.property_details_page", {"property": property}
        )
