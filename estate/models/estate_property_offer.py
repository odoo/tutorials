from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    price = fields.Float()
    status = fields.Selection([
        ('accepted', "Accepted"),
        ('refused', "Refused")
    ], copy=False)

    property_id = fields.Many2one('estate.property', required=True)
    partner_id = fields.Many2one('res.partner', required=True)
