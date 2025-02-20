from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'the offer of the property being sold'

    price = fields.Float()
    status = fields.Selection(selection = [('accepted', 'Accepted'), ('refused', 'Refused')], copy = False)
    partner_id = fields.Many2one('res.partner', string = 'Partner', required = True)
    property_id = fields.Many2one('estate.property', string = 'Property', required = True)
