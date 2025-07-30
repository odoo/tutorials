from odoo import http
from odoo.addons.estate.controllers.estate_property import EstatePropertyController

class EstateAuction(EstatePropertyController):
    @http.route(["/properties", "/properties/page/<int:page>"], type="http", auth="user", website=True)
    def property_list(self, page=1, domain=None, status="all", min_price=None, max_price=None, listed_after=None, sell_type="all", **kwargs):
        domain = domain or []
        if sell_type in ["auction", "regular"]:
            domain = [("sell_type", '=', sell_type)]
        return super().property_list(page=page, domain=domain, status=status, min_price=min_price, max_price=max_price, listed_after=listed_after, **kwargs)
        