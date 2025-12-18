from odoo import fields, models


class Offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float("Offer Price")
    status = fields.Selection(
        string="Status",
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
        copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
