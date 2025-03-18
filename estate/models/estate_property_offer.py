from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "My Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([('accept', 'Accept'), ('refused', 'Refused')], copy = False)
    partner_id = fields.Many2one('res.partner', string = "Partner", required = True)
    property_id = fields.Many2one('estate_property', string = 'Property', required = True)