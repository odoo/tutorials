from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer description"

    price = fields.Float('price')
    status = fields.Selection(
        string='status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
