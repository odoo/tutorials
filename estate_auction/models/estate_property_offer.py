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
            if offer.property_id:
                offer.is_auction = offer.property_id.sale_type == "auction"
            else:
                offer.is_auction = False

    @api.model_create_multi
    def create(self, vals_list):
        offers = super(EstatePropertyOfferAuction, self).create(vals_list)
        for offer in offers:
            if offer.property_id:
                offer.property_id._compute_highest_offer()
        return offers
    @api.depends("property_id.sale_type")
    def _compute_auction_offer_invisible(self):
        for offer in self:
            # If property exists and its sale_type is 'auction', then hide the buttons.
            offer.auction_offer_invisible = offer.property_id and (offer.property_id.sale_type == "auction")

    @api.model_create_multi
    def create(self, vals_list):
        """
        1) Perform our own validation:
           - If sale_type == 'auction': Offer >= expected_price
           - Else (regular): Offer > best_offer
        2) Bypass the parent's create by calling super(models.Model, self).create(...)
           to skip the parent's 'must exceed best_offer' check for auctions.
        3) Update property state to 'offer_received' if it's 'new' or already 'offer_received'.
        4) Recompute highest_offer after creation.
        """
        new_records = self.env["estate.property.offer"].browse()
        for vals in vals_list:
            # Must have a property_id
            property_id = vals.get("property_id")
            if not property_id:
                raise ValidationError(_("Property ID is required to create an offer."))

            prop = self.env["estate.property"].browse(property_id)

            # Disallow offers if property is in a terminal state
            if prop.state in ["offer_accepted", "sold", "cancelled"]:
                raise UserError(
                    _("Cannot create an offer. The property is already '%s'.")
                    % prop.state.replace("_", " ").title()
                )

            # Auction logic
            if prop.sale_type == "auction":
                # Skip best_offer check, only enforce >= expected_price
                if vals.get("price", 0.0) < prop.expected_price:
                    raise ValidationError(
                        _("Auction offers must be at least the expected price: %.2f")
                        % prop.expected_price
                    )
            else:
                # Regular logic: must exceed best_offer
                if vals.get("price", 0.0) < prop.best_offer:
                    raise ValidationError(
                        _("The offer must be higher than %.2f.") % prop.best_offer
                    )

            # Update property state
            if prop.state in ["new", "offer_received"]:
                prop.sudo().state = "offer_received"

            # Create record using the BASE model's create to bypass parent's create method
            record = super(models.Model, self).create([vals])
            new_records |= record

        # Recompute highest offer on each property
        for rec in new_records:
            if rec.property_id:
                rec.property_id._compute_highest_offer()

        return new_records
