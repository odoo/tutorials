from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description = 'estate property offer'

    price = fields.Float()
    status = fields.Selection(selection=(('accepted', 'Accepted'), ('refused', 'Refused')), copy=False)
    partner_id = fields.Many2one('res.partner', required=True, string='Partner')
    property_id = fields.Many2one('estate_property', required=True)
