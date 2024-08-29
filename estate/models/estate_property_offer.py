from datetime import timedelta
from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    # model definition
    _name = "estate.property.offer"
    _description = "property offer model"

    # normal fields
    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)

    # relations
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    # computed
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # computing methods
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                delta = record.date_deadline - fields.Date.today()
                record.validity = delta.days

    # action methods (assigned to buttons)
    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'

    # the buyer of the property set to the offer's partner
    # the selling price of the property set to the price of the offer
    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
