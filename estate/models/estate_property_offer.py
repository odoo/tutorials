from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "ESTATE property tag"

    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id, required=True)
    price = fields.Monetary(currency_field='currency_id')
    status = fields.Selection([("Accepted", "Accepted"), ("Refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", required=True)
