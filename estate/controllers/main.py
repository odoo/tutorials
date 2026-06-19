from odoo import http
from odoo.http import request


class EstateController(http.Controller):
    @http.route("/properties", auth="public", type="http", website=True)
    def property_list(self, **kwargs):
        properties = request.env["estate.property"].search([])
        return request.render(
            "estate.property_list_template",
            {
                "properties": properties,
            },
        )

    @http.route(
        "/properties/<int:property_id>", auth="public", type="http", website=True
    )
    def property_detail(self, property_id, **kwargs):

        property_record = request.env["estate.property"].browse(property_id)

        return request.render(
            "estate.property_detail_template",
            {
                "property": property_record,
            },
        )
