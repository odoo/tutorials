from odoo import fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"

    price = fields.Float('Price', copy=False)
    state = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        required=True
    )
    partner_id = fields.Many2one('res.partner', string='Buyer', reuired=True)
    property_id = fields.Many2one("estate.property", string="Property", reuired=True)
