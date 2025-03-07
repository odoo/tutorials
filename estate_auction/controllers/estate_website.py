from odoo import http
from odoo.addons.estate.controllers.estate_website import EstateWebsite


class EstateAuctionWebsite(EstateWebsite):
    @http.route(['/property', "/property/page/<int:page>"], type="http", auth="public", website=True)
    def list_properties(self, page=1, status="all", min_price=None, max_price=None, domain=None, property_sale_format="all", **kwargs):
        domain = domain or []
        if property_sale_format in ["auction", "regular"]:
            domain = [('property_sale_format', '=', property_sale_format)]
        return super().list_properties(page=page, status=status, min_price=min_price, max_price=max_price, domain=domain, **kwargs)
