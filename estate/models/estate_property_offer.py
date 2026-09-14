from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "It is a estate property offer model"

    price = fields.Float()
    status = fields.Selection([("Accepted", "Accepted"), ("Refuse", "Refuse")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
