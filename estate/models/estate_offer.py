from odoo import models, fields


class EstateOffer(models.Model):
    _name = 'estate.offer'
    _description = 'Estate Offer'

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate', required=True)
