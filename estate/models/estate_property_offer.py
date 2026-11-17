from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    property_id = fields.Many2one(
        comodel_name='estate.property',
        string="Property",
        required=True,
        index=True,
    )
