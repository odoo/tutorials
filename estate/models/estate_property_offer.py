from odoo import fields, models  # ty: ignore[unresolved-import]


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for a property by buyer"

    price = fields.Float()
    status = fields.Selection(
        string="Offer Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
