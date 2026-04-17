from odoo import fields, models


class EstatePropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = "A  model where offer for the properties are stored"

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('accepted', "Accepted"),
                              ('refused', "Refused")],
                              required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one(
        'estate.property', required=True)
