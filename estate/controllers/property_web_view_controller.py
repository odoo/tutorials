from odoo import http
from odoo.http import request


class PropertyWebView(http.Controller):
    @http.route(["/properties", "/properties/page/<int:page>"], type="http", auth="public", website=True)
    def show_properties(self, page=1):
        step = 6
        offset = (page - 1) * step

        properties = (
            request.env["estate.property"].sudo().search(
                [
                    "&",
                    ("state", "in", ["new", "offer_received", "offer_accepted"]),
                    ("active", "=", True),
                ],
                limit=step,
                offset=offset,
            )
        )

        total_properties = request.env["estate.property"].sudo().search_count(
            [
                "&",
                ("state", "in", ["new", "offer_received", "offer_accepted"]),
                ("active", "=", True),
            ]
        )

        pager = request.website.pager(
            url="/properties", total=total_properties, step=step, page=page
        )

        return request.render(
            "estate.estate_property_web_view", {"properties": properties, "pager": pager}
        )


    @http.route(["/property/<int:id>"], type="http", auth="public", website=True)
    def show_property_by_ID(self, id):
        property = request.env['estate.property'].sudo().search([('id', '=', id)])

        if property:
            return request.render('estate.estate_property_web_view_single', {
                'property': property
            })
