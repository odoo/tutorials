from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"  # Descending order of price

    price = fields.Float(string="Offer Price", required=True, default=0.0)
    validity = fields.Integer(string="Validity (days)", default=7)
    validity_date = fields.Date(string="Validity Date", compute="_compute_validity_date", inverse="_inverse_validity_date", store=True)

    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", copy=False)
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    @api.depends("validity")
    def _compute_validity_date(self):
        for record in self:
            record.validity_date = record.create_date + timedelta(days=record.validity) if record.create_date

    def _inverse_validity_date(self):
        for record in self:
            if record.validity_date and record.create_date:
                record.validity = (record.validity_date - record.create_date.date()).days

    def action_accept(self):
        # Accept an offer and update property state accordingly.
        for record in self:
            if record.property_id.selling_price:
                raise UserError("An offer has already been accepted for this property!")

            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'  # Update property state

    def action_refuse(self):
        # Refuse an offer.
        for record in self:
            record.status = 'refused'
