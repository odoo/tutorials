from datetime import timedelta
from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    # Fields declaration
    price = fields.Float("Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )

    # Compute and inverse methods in order of field declaration
    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = (
                offer.create_date or fields.Datetime.today()
            ) + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            create_date = fields.Date.from_string(offer.create_date)
            offer.validity = (offer.date_deadline - create_date).days

    # Action methods
    def offer_confirm(self):
        if float_is_zero(self.property_id.selling_price,precision_digits=2):
            if self.price > self.property_id.expected_price * 0.9:
                self.status = "accepted"
                self.property_id.partner_id = self.partner_id
                self.property_id.selling_price = self.price
                self.property_id.state = "offer_accepted"
            else:
                raise UserError(f"Selling price must be at least 90% greater than expected price.")
        else:
            raise UserError("you can select only one offer for one property.")
        

    def offer_cancel(self):
        self.status = "refused"
        self.property_id.partner_id = ""
        self.property_id.selling_price = 0
        self.property_id.state = "offer_received"

    # SQL constraints
    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price >= 0)",
            "The price must be strictly positive.",
        )
    ]
