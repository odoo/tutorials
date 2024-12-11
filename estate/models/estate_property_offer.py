from odoo import models, fields, api
from datetime import date, timedelta

class estatePropertyOffer(models.Model):
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