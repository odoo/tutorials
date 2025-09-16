from datetime import date
from odoo import api, models, fields

from odoo.orm.domains import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"

    price = fields.Float("Price")
    status = fields.Selection(
        [('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = date.today() + timedelta(record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - date.today()).days
