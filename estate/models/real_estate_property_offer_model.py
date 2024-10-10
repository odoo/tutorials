
from odoo import fields, models


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"

    price = fields.Float()
    status = fields.Selection( 
        string = 'Status',
        selection = [('accepted','Accepted'),('refused','Refused')],
        copy = False
    )
    partner_id = fields.Many2one('res.partner',string = "Buyer", required=True)
    property_id = fields.Many2one('estate_property',string="Property", required=True)