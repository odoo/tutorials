from odoo import fields, api, models  # type: ignore
from datetime import timedelta
from odoo.exceptions import UserError  # type: ignore


class EstatePropertiesOffer(models.Model):
    _name = 'estate.properties.offer'
    _description = "Estate Properties Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[(
        'accepted', 'Accepted'), ('refused', 'Refused'), ],)
    partner_id = fields.Many2one(
        'res.partner', string='Partner', index=True,  copy=False, required=True)
    property_id = fields.Many2one(
        'estate.properties', string='Property', index=True,  copy=False, required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('price', 'CHECK(price > 0)',
         'Offer Price should be greater than 0'),
    ]

    @api.depends('property_id.date_availability', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.property_id.date_availability + \
                timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline -
                               record.property_id.date_availability).days

    def accept_offer(self):
        for record in self:
            if record.property_id.selling_price > 0 or record.status == "accepted":
                raise UserError("Offer already accepted")
            record.status = "accepted"
            record.property_id.state = 'offer_accepted'
            record.property_id.partner_id = record.partner_id
            record.property_id.selling_price = record.price

    def refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.selling_price = 0.00
                record.property_id.partner_id = 0
            record.status = "refused"
            record.property_id.state = 'cancelled'
