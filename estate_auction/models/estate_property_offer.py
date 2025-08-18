from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOfferAuction(models.Model):
    _inherit = "estate.property.offer"

    is_auction = fields.Boolean(
        string="Is Auction",
        compute="_compute_is_auction",
        store=True
    )
    auction_offer_invisible = fields.Boolean(
        string="Auction Offer Buttons Invisible",
        compute="_compute_auction_offer_invisible",
        store=True
    )
    is_auction_property = fields.Boolean(
        string="Is Auction Property",
        related="property_id.is_auction",
        store=True
    )

    @api.depends("property_id.sale_type")
    def _compute_is_auction(self):
        for offer in self:
            offer.is_auction = offer.property_id.sale_type == "auction" if offer.property_id else False

    @api.depends("property_id.sale_type")
    def _compute_auction_offer_invisible(self):
        for offer in self:
            offer.auction_offer_invisible = offer.property_id and offer.property_id.sale_type == "auction"

    @api.model_create_multi
    def create(self, vals_list):
        new_records = self.env["estate.property.offer"].browse()

        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price", 0.0)

            if not property_id:
                raise ValidationError(_("Property ID is required to create an offer."))

            prop = self.env["estate.property"].browse(property_id)

            if prop.state in ["offer_accepted", "sold", "cancelled"]:
                raise UserError(_("Cannot create an offer. The property is not open for new offers."))

            if prop.sale_type == "auction":
                if price < prop.expected_price:
                    raise ValidationError(_("Auction offers must be at least the expected price."))
            else:
                if price < prop.best_offer:
                    raise ValidationError(_("The offer must be higher than the current best offer."))

            if prop.state in ["new", "offer_received"]:
                prop.sudo().state = "offer_received"

            record = super().create([vals])
            new_records |= record

        for rec in new_records:
            if rec.property_id:
                rec.property_id._compute_highest_offer()

        return new_records
