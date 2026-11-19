from odoo import fields, models


class EstatePorpertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'), ('refused', 'Refused')
    ])
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    Property_id = fields.Many2one("estate.property", "Property", required=True)
