from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    """Offers for the property"""

    _name = "estate.property.offer"
    _description = "Property Offers"
    _order = "price desc"

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "offer price must be positive")
    ]

    price = fields.Float(
        string="Offer Price",
        help="Price for the offer"
    )
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        help="Current status of the property",
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
        help="Partner assigned for the sale"
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
        help="Property for sale"
    )
    validity = fields.Integer(
        string="Validity",
        default=7,
        help="Validity period of the offer"
    )
    date_deadline = fields.Date(
        string="Date Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )
    create_date = fields.Date(
        string="Create Date",
        default=fields.Date.context_today
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        """Compute deadline date based on create_date and validity period."""
        for record in self:
            record.date_deadline = (
                record.create_date + timedelta(days=record.validity)
                if record.create_date else False
            )

    def _inverse_date_deadline(self):
        """Inverse function to calculate validity from date_deadline."""
        for record in self:
            record.validity = (
                (record.date_deadline - record.create_date).days
                if record.date_deadline else 7
            )
    
    def action_confirm(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("Property is already Sold")
            accepted_offer = record.property_id.offer_ids.filtered(
                lambda x: x.status == 'accepted'
            )
            if accepted_offer:
                raise UserError("Only one offer can be accepted")
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
    
    def action_cancel(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.buyer_id = False
                record.property_id.selling_price = 0.0
            record.status = 'refused'
