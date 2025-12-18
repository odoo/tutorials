from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "A property offer"

    price = fields.Float('Price')
    status = fields.Selection(selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
        ], copy=False, string='Status')
    property_buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)