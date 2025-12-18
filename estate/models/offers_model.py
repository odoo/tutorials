from odoo import models, fields


class offers_model(models.Model):
    _name = "estate.offers"
    _description = "Offers Model"

    price = fields.Integer(required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        required=True,
    )
    building_id = fields.Many2one("estate.buildings", string="Building")
    partner_id = fields.Many2one("res.partner", string="Partner")
