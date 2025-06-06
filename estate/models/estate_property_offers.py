from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffers(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(required=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("cancelled", "Cancelled"),
        ],
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", required=True
    )
    property_id = fields.Many2one(
        comodel_name="estate.property", string="Property", required=True,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be positive."),
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.validity:
                offer.date_deadline = fields.Date.add(
                    fields.Date.today(), days=offer.validity
                )
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - fields.Date.today()).days
            else:
                offer.validity = 0

    def action_offer_tick(self):
        for record in self:
            if float_compare(record.property_id.expected_price * 0.9, record.price, precision_digits=2) > 0:
                raise ValidationError(
                    "The offer price must be at least 90% of the expected price."
                )
            elif not record.property_id.selling_price:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "offer_accepted"
                return True
            else:
                raise UserError("The offer for this property is already accepted.")
        return False

    def action_offer_cross(self):
        for record in self:
            if record.status == "accepted":
                record.status = "refused"
                record.property_id.state = "offer_received"
                record.property_id.buyer_id = False
                record.property_id.selling_price = 0.0
        return True

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        for record in self:
            record.property_id.selling_price = 0.0
