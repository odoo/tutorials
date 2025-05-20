import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class EstateAuctionController(http.Controller):
    
    @http.route("/property/offer_form/<int:property_id>", type="http", auth="public", website=True)
    def property_offer_form(self, property_id):
        try:
            property = request.env["estate.property"].browse(property_id)
            offer_exists = property.offer_ids.filtered(lambda offer: offer.partner_id == request.env.user.partner_id)
            return request.render("estate_auction.property_make_offer_form", {"property": property, "offer_exists": offer_exists})
        except Exception as err:
            return self._acknowledge_buyer("danger", "Error", err, property.id)

    @http.route("/property/make_offer", type="http", auth="user", website=True, methods=["POST"], csrf=True)
    def property_make_offer_form(self, **vals):
        try:            
            if float(vals.get("offer_amount")) <= float(vals.get("property_expected_price")):
                return self._acknowledge_buyer("danger", "Invalid Offer Amount", "Offer amount must be greater than expected price.", vals.get("property_id"))
            
            request.env["estate.property.offer"].sudo().create({
                "price": float(vals.get("offer_amount")),
                "partner_id": request.env.user.partner_id.id,
                "property_id": int(vals.get("property_id"))
            })
            
            return self._acknowledge_buyer("success", "Offer created", "Congratulations !! Your offer has been submitted we will notify you as soon as auction concludes.", vals.get("property_id"))
        except Exception as err:
            _logger.error(err)
            return self._acknowledge_buyer("danger", "Error", err, vals.get("property_id"))

    def _acknowledge_buyer(self, message_type, message_title, message, property_id=False):
        return request.render("estate_auction.message_template", {
            "message_type": message_type,
            "message_title": message_title,
            "message": message,
            "property_id": property_id
        })
