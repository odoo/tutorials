from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "this is the estate property offer model"
    price = fields.Float(digits=(20,2))
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    status = fields.Selection(selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    _sql_constraints = []
