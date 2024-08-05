from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    # name = fields.Char(string='Name', required=True)
    price = fields.Float(string="Price")
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy="False",
        help="Status of the Offer")
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required="True",
        help='Person making the offer'
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property ID',
        required="True"
    )
