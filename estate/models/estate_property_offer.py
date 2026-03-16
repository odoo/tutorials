from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(
        string="Offer Status",
        selection=[
            ("offer_accepted", "Accepted"),
            ("offer_refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
