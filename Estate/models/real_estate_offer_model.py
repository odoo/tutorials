from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    name = fields.Char(required=True)
    price = fields.Float()
    status = fields.Selection([('Accepted', 'accepted'), ('Refused', 'refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate_property', required=True)
