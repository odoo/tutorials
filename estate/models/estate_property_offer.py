from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offers'

    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    price = fields.Float()
    property_id = fields.Many2one(comodel_name='estate.properties', required=True, readonly=True)
    status = fields.Selection(
        [
            ('refused', "Refused"),
            ('accepted', "Accepted")
        ],
        copy=False
    )
