import logging

from odoo import api, fields, models
from odoo.tools import date_utils


class EstatePropertyOffer(models.Model):
    _name: str = "estate.property.offer"
    _description: str | None = None
    _order = "price desc"

    price: fields.Float = fields.Float()
    status: fields.Selection = fields.Selection([(word.lower(), word) for word in ['Accepted', 'Refused']], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    date_deadline: fields.Date = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    validity = fields.Integer()
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'Prices must be positive',
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = date_utils.add(fields.Date.today(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.today()).days

    def accept(self):
        self.status = "accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price

    def deny(self):
        self.status = "refused"
