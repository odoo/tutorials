from odoo import models, fields


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _descreption = "the offer of estate property"

    price = fields.Float("Price")
    partner_id = fields.Many2one("res.partner", required=True)
    partner_id = fields.Many2one('estate.property', required=True)
    status = fields.Selection(
        [
            ("Accepted", "Accepted"),
            ("Refused", "Refused")
        ],
        copy=False
    )
