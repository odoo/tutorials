from odoo import fields, models


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Propert offers"

    price = fields.Float(string="Price")
    status = fields.Selection(
        copy="False",
        selection=[
            ("acctepted", "Acctepted"),
            ("refused", "Refused"),
        ],
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
