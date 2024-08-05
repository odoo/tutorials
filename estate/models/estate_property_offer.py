from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offers that propeties receive.'

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ])
    partner_id = fields.Many2one('res.partner', required=True, string='Partner')
    property_id = fields.Many2one('estate.property', required=True)
