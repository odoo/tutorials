from odoo import http
from odoo.http import request

class MyController(http.Controller):
    @http.route(["/properties", "/properties/page/<int:page>"], type="http", auth="public", website=True)
    def handler(self, page=1, **kwargs):
        filter_key = request.params.get("filter")
        def get_filter(domain_filter):
            if domain_filter == "available":
                return [("state", "not in", ["sold", "cancelled"]), ("active", "=", True)]
            elif domain_filter == "sold":
                return [("state", "=", "sold")]
            else:
                return []
        domain = get_filter(filter_key)
        property = request.env["estate.property"].sudo()
        properties_count = property.search_count(domain)
        page_size = 9
        pager = request.website.pager(
            url="/properties",
            total=properties_count,
            page=page,
            step=page_size,
            url_args={ "filter": filter_key }
        )
        properties = property.search(domain, limit=page_size, offset=pager["offset"])
        return request.render("estate.property_template", {
            "properties": properties,
            "pager": pager,
            "current_filter": filter_key
        })

    @http.route("/property/<int:property_id>", auth="public", website=True)
    def property_detail(self, property_id):
        property = request.env["estate.property"].sudo().browse(property_id)
        if not property.exists():
            return request.not_found()
        return request.render("estate.property_details_template", { "property": property })
