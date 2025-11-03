from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    
    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.to_date(record.create_date) + relativedelta(days=record.validity)
            else:
                record.date_deadline = 0

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days
            else:
                record.validity = 0

    def action_accept(self):
        for record in self:
            if record.property_id.buyer:
                raise UserError("Property already accepted")
            else:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.state = 'offer_accepted'
                record.property_id.buyer = record.partner_id

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("Property already accepted")
            else: 
                record.status = 'refused'
