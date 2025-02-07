from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer model'


    price = fields.Float('Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    property_id = fields.Many2one(comodel_name='estate.property', required=True)
