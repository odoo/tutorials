from odoo import fields,models

class EstatePropertytOffer(models.Model):
    _name = "estate.property.offer"
    _description ="It defines the estate property Offer"

    name= fields.Char(required=True)
    price= fields.Float(copy=False, string='Price')
    status= fields.Selection(selection=[('Accepted','Accepted'), ('Refused','Refused')], string='Status')
    partner_id= fields.Many2one('res.partner', string="Partner")
    property_id= fields.Many2one('estate.property', string='Property')
