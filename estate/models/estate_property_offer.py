from odoo import fields, models  # type: ignore

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Ayve"

    price = fields.Float()
    status = fields.Selection(
    [
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ],
    string='Status',
    copy=False
    )
    partner_id = fields.Many2one('res.partner',required=True,string="Partner")
    property_id = fields.Many2one('estate.property',required=True, string="Property ID")

    