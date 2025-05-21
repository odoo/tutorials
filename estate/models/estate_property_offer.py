from odoo import fields, models

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer made by a potential buyer"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
