from odoo import fields, models

class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Offer"

    price = fields.Float(string="Offer Price")
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
        string="Status"
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)