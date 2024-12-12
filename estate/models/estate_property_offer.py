from odoo import models, fields, api # type: ignore
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offers'

    price = fields.Float()
    partner_id = fields.Many2one('res.partner', string = 'Partner', required = True)
    property_id = fields.Many2one('estate.property', string = 'Property Name', required = True)
    status = fields.Selection(selection = [('refused', 'Refused'), ('accepted', 'Accepted')], copy = False)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = '_compute_deadline', inverse = '_compute_validity')

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = date.today() + timedelta(record.validity)

    def _compute_validity(self):
        for record in self:
            record.validity = (record.date_deadline - date.today()).days

    def action_accept(self):
        for record in self:
            for offer in record.property_id.offers_id:
                offer.status = 'refused'
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.state = 'new'
