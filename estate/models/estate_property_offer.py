from datetime import datetime, timedelta

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(
        string="Price",
        help="The price offered for the property.",
    )

    status = fields.Selection(
        string="Status",
        help="The status of the offer.",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )

    partner_id = fields.Many2one(
        string="Partner",
        help="The partner who made the offer.",
        required=True,
        comodel_name="res.partner",
    )

    property_id = fields.Many2one(
        string="Property",
        help="The property the offer is for.",
        required=True,
        comodel_name="estate.property",
    )

    validity = fields.Integer(
        string="Validity (days)",
        help="The number of days the offer is valid for.",
        default=7,
    )

    date_deadline = fields.Date(
        string="Deadline",
        help="The date the offer expires.",
        compute="_compute_validity",
        inverse="_inverse_validity",
    )

    # -------------------------------------------------------------------------
    # SQL QUERIES
    # -------------------------------------------------------------------------

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)', 'The price must be positive.'),
    ]

    # -------------------------------------------------------------------------
    # COMPUTED FIELDS
    # -------------------------------------------------------------------------

    @api.depends("validity")
    def _compute_validity(self):
        for record in self:
            record.create_date = record.create_date or datetime.now().date()
            record.date_deadline = datetime.now().date() + timedelta(days=record.validity)

    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # -------------------------------------------------------------------------

    @api.onchange('price')
    def _onchange_price(self):
        if self.price == 0:
            return
        if self.price <= 0:
            raise ValidationError("The price must be positive.")

    # -------------------------------------------------------------------------
    # ACTION METHODS
    # -------------------------------------------------------------------------

    def _inverse_validity(self):
        for record in self:
            record.create_date = record.create_date or datetime.now().date()
            record.validity = (record.date_deadline - datetime.now().date()).days

    def action_confirm(self):
        if any(offer.status == "accepted" for offer in self.property_id.offer_ids):
            raise UserError("Offer already accepted.")

        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        for offer in self.property_id.offer_ids.filtered(lambda o: o != self):
            offer.status = "refused"

    def action_cancel(self):
        self.status = "refused"
        if any(offer.status == "accepted" for offer in self.property_id.offer_ids):
            return
        self.property_id.selling_price = 0.0
        self.property_id.buyer_id = False

    # -------------------------------------------------------------------------
    # CONSTRAINTS METHODS
    # -------------------------------------------------------------------------

    rounding_precision = 0.0001
    @api.constrains('price')
    def _check_price(self):
        compare_value = float_compare(self.price,0.9*self.property_id.expected_price,precision_digits=2)
        if compare_value == -1:
                raise UserError("Offer Price must be atleast 90% of the expected price.")
        return True
