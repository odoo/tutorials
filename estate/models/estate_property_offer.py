from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate properties offer"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'),
        ('refused', 'Refused')],
        help="Status of the offer",
        copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
