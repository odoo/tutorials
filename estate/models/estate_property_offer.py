from odoo import fields, models

class estate_property_offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'property offer'

    price = fields.Float(string = 'price')
    status = fields.Selection([('accepted', 'Accepted'),
            ('refused', 'Refused')], string = 'status')
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', required=True)
