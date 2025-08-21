from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([("Accepted","accepted"),("refused","Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    