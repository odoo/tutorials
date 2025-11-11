from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
    )

    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
    @api.constrains("price")
    def _check_price_ratio(self):
        for record in self:
            if record.price <= 0.0:
                raise ValidationError("Price must be greater than 0")

    _check_price = models.Constraint(
        'CHECK(price < 0)',
        'The price must be strictly positive.'
    )