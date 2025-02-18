from odoo import http
from odoo.http import request


class EstateController(http.Controller):
    @http.route("/properties", auth="public", website=True)
    def handler(self):
        properties = (
            request.env["estate.property"]
            .sudo()
            .search([("status", "not in", ["sold", "cancelled"])])
        )

        return request.render("estate.property_template", {"properties": properties})

    @http.route("/property/<int:property_id>", auth="public", website=True)
    def property_detail(self, property_id):
        property = request.env["estate.property"].sudo().browse(property_id)

        if not property.exists():
            return request.not_found()

        return request.render(
            "estate.property_details_template", {"property": property}
        )
