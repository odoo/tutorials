from odoo import models, fields # type: ignore

class estatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "This is offer table"

    price = fields.Float(required=True)
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        required=True
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True
    )
    