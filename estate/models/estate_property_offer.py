from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name: str = "estate.property.offer"
    _description: str | None = None

    price: fields.Float = fields.Float()
    status: fields.Selection = fields.Selection([(word.lower(), word) for word in ['Accepted', 'Refused']], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
