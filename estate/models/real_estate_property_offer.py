from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.offer"
    _description = "Test-tag"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("real_estate", string="Property", required=True)
