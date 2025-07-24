from odoo import fields, models


class EstateProperties(models.Model):
    _name = "estate.property.offer"
    _description = " Estate Property Offers"

    price = fields.Float("Price")
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
