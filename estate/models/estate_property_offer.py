from odoo import fields, models


class propertyTag(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for the Real Estate Property"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    property_id = fields.Many2one('estate.property', string="Property")
