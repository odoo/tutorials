from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate_property.offer"
    _description = "Offer to the Estate"

    name = fields.Char('Nom', required=True)
    price = fields.Float('Price')
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ]
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate_property', string="Property", required=True)



    