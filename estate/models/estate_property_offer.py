from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.date_utils import relativedelta
from odoo.tools.float_utils import float_compare

PROPERTY_OFFER_STATE = [("accepted", "Accepted"), ("refused", "Refused")]


class PropertyOffer(models.Model):

    # -------------------------------------------------------------------------
    # Private attributes
    # -------------------------------------------------------------------------
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    # -------------------------------------------------------------------------
    # Field declarations
    # -------------------------------------------------------------------------
    price = fields.Float()
    status = fields.Selection(selection=PROPERTY_OFFER_STATE, copy=False)

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    # -------------------------------------------------------------------------
    # SQL constraints
    # -------------------------------------------------------------------------
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        "The offer price must be strictly positive."
    )

    # -------------------------------------------------------------------------
    # Compute and inverse methods
    # -------------------------------------------------------------------------
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = base_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - base_date).days

    # -------------------------------------------------------------------------
    # ORM methods
    # -------------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_record = self.env["estate.property"].browse(val.get("property_id"))

            existing_prices = property_record.offer_ids.mapped("price")
            max_property_offers = max(existing_prices) if existing_prices else 0
            if float_compare(val.get("price"), max_property_offers, precision_digits=2) <= 0:
                raise UserError(f"The offer must be higher than {max_property_offers}")
            if property_record.state == "new":
                property_record.state = "offer_received"
        return super().create(vals)

    # -------------------------------------------------------------------------
    # Action methods
    # -------------------------------------------------------------------------
    def action_accept_offer(self):
        for offer in self:
            offer.property_id.offer_ids.status = "refused"
            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "offer_accepted"
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
        return True
