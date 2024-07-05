from odoo import models, fields


class estate_offer(models.Model):
    _name = "estate.property.offer"
    _description = "This is Real Estate property offer"

    price = fields.Float("Price")
    status = fields.Selection(
        string="status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
