# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, fields
from odoo.http import request, AccessError, UserError
from odoo.addons.estate.controllers.main import PropertyController


class PropertyController(PropertyController):

    @http.route(["/properties/<int:property_id>/create-offer", "/property/<int:property_id>/create-offer"], type="http", auth="public", website=True)
    def create_offer(self, property_id, **kwargs):
        domain = [
            ("active", "=", True),
            ("state", "in", ["new", "offer_received"]),
            ("id", "=", property_id),
            ("auction_start_time", "!=", False),
            ("auction_state", "=", "blocked")
        ]
        property = request.env["estate.property"].sudo().search(domain)
        user = request.env.user
        if not property:
            raise AccessError("Invalid access to property")
        success = kwargs.get("success")
        if request.httprequest.method == "POST":
            partner_name = kwargs.get("partner_name")
            try:
                partner_amount = int(kwargs.get("partner_amount"))
            except ValueError:
                raise UserError("Invalid Partner Amount")
            if partner_amount <= 0:
                raise UserError("Invalid Partner Amount")
            if not partner_name:
                raise UserError("Invalid Partner Name")
            partner = user.partner_id
            if not partner or not partner.active:
                partner = request.env["res.partner"].sudo().create({"name": partner_name})
            request.env["estate.property.offer"].sudo().create({
                "property_id": property_id,
                "partner_id": partner.id,
                "price": partner_amount,
            })
            return request.redirect(f"/properties/{property_id}/create-offer?success=True")
        return request.render("estate_auction.create_offer_view", {"property": property, "user": user, "success": success})

    def _get_filter_domain(self, **kwargs):
        domain = super()._get_filter_domain(**kwargs)
        auction_available = kwargs.get("auction_available")
        if auction_available:
            domain.append(("auction_state", "=", "blocked"))
            domain.append(("auction_end_time", ">", fields.Datetime.now()))
        return domain

    def _get_url_args(self, **kwargs):
        url_args = super()._get_url_args(**kwargs)
        url_args["auction_available"] = kwargs.get("auction_available")
        return url_args
