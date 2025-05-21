from odoo import fields, models


class TestModel(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Model Offer'

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
