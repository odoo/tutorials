from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):

    @http.route(
        ["/properties", "/properties/<int:page_no>"],
        type="http",
        auth="public",
        website=True,
    )
    def properties_list(self, page_no=1, **kwargs):
        props = request.env["estate.property"].search(
            [("state", "in", ["offer_received", "offer_accepted"])]
        )
        properties_per_page = 6

        offset = (page_no - 1) * properties_per_page

        totalPage = (len(props) - 1) // 6
        properties = props.search(
            [
                ("state", "in", ["offer_received", "offer_accepted"]),
            ],
            limit=properties_per_page,
            offset=offset,
        )

        return request.render(
            "estate.property_controller",
            {
                "properties": properties,
                "page_no": page_no,
                "totalPage": totalPage + 1,
            },
        )

    @http.route("/property/<int:record_id>", type="http", auth="public", website=True)
    def get_record(self, record_id, **kwargs):
        print("record id found")
        property = request.env["estate.property"].sudo().browse(record_id)

        if not property.exists():
            print("record does not found")
            return request.not_found()
        print("record found")
        return request.render(
            "estate.template_property_details",
            {
                "property": property,
            },
        )
