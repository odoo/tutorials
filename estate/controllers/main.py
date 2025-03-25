# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, fields
from odoo.http import request
from odoo.exceptions import AccessError


class PropertyController(http.Controller):
    @http.route(["/properties/page/<int:page>", "/properties", "/property"], type="http", auth="public", website=True)
    def properties(self, page=1, **kwargs):
        limit = 6
        EstateProperty = request.env["estate.property"].sudo()
        domain = self._get_filter_domain(**kwargs)
        url_args = self._get_url_args(**kwargs)
        property_count = EstateProperty.search_count(domain)
        pager = request.website.pager(
            url="/properties",
            url_args=url_args,
            total=property_count,
            page=page,
            step=limit
        )
        property_filters = url_args
        properties = EstateProperty.search(domain=domain, limit=limit, offset=pager["offset"])
        return request.render("estate.estate_properties_grid", {
            "properties": properties,
            "pager": pager,
            "property_filters": property_filters
        })

    @http.route(["/property/<int:property_id>", "/properties/<int:property_id>"], type="http", auth="public", website=True)
    def view_property(self, property_id):
        domain = [("active", "=", True), ("state", "in", ["new", "offer_received"]), ("id", "=", property_id)]
        property = request.env["estate.property"].sudo().search(domain)
        if not property:
            raise AccessError("Cannot access the property")
        return request.render("estate.single_property_view", {"property": property})

    def _get_filter_domain(self, **kwargs):
        domain = [("active", "=", True), ("state", "in", ["new", "offer_received"])]
        listed_after = kwargs.get("listed_after")
        try:
            listed_after_date = fields.Date.to_date(listed_after)
            if listed_after_date:
                domain.append(("create_date", ">=", listed_after_date))
        except ValueError:
            pass
        return domain

    def _get_url_args(self, **kwargs):
        return {"listed_after": kwargs.get("listed_after", "")}
