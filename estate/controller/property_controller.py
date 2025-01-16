from odoo import http
from odoo.http import request

class PropertyController(http.Controller):
    
    @http.route(["/properties", "/properties/page/<int:page>"], type="http", auth="public", website=True)
    def show_properties(self, page=1):
        step = 6
        offset = (page - 1) * step

        properties = (
            request.env["estate.property"]
            .sudo()
            .search(
                [
                    "&",
                    ("state", "in", ["new", "offer received", "offer accepted"]),
                    ("active", "=", True),
                ],
                limit=step,
                offset=offset,
            )
        )

        total_properties = request.env["estate.property"].sudo().search_count(
            [
                "&",
                ("state", "in", ["new", "offer received", "offer accepted"]),
                ("active", "=", True),
            ]
        )

        pager = request.website.pager(
            url="/properties", total=total_properties, step=step, page=page
        )

        return request.render(
            "estate.estate_property_web_view", {"properties": properties, "pager": pager}
        )
        
    @http.route('/properties/<int:property_id>', type='http', auth='public', website=True)
    def property_details(self, property_id):
        property = request.env['estate.property'].browse(property_id)
        
        return request.render('estate.property_details_template',{
            'property': property
        })

    
