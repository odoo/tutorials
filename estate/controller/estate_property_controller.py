from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):

    @http.route(["/properties"], type="http", auth="public", website=True)
    def properties_list(self, page=1, **kwargs):
        try:
            page = int(page)
        except ValueError:
            page = 1
        Property = request.env["estate.property"].sudo()
        properties_per_page = 6

        total_properties = Property.search_count(
            [
                ("state", "in", ["offer received", "offer accepted"]),
            ]
        )
        total_pages = (
            total_properties + properties_per_page - 1
        ) // properties_per_page
        page = max(1, min(page, total_pages))
        offset = (page - 1) * properties_per_page
        properties = Property.search(
            [
                ("state", "in", ["offer received", "offer accepted"]),
            ],
            limit=properties_per_page,
            offset=offset,
        )
        return request.render(
            "estate.property_template",
            {
                "properties": properties,
                "page": page,
                "total_pages": total_pages,
            },
        )

    @http.route("/properties/<int:record_id>", type="http", auth="public", website=True)
    def get_record(self, record_id, **kwargs):
        record = request.env["estate.property"].sudo().browse(record_id)
        if not record.exists():
            return request.not_found()
        return request.render(
            "estate.property_view_details",
            {"record": record},
        )
