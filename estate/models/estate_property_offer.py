from odoo import models, fields, api
from datetime import datetime

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Real Estate Property Offers"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False
    )

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate_property', required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for rec in self:
            create_date = rec.create_date or fields.Datetime.now()
            rec.date_deadline = fields.Date.add(create_date, days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            create_date = rec.create_date or fields.Datetime.now()
            rec.validity = (rec.date_deadline - create_date.date()).days


