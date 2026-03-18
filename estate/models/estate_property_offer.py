from odoo import models, fields

class EstatePropertyOffer (models.Model):
    _name = "estate.property.offer"
    _description = "Lời đề nghị"
    
    price = fields.Integer( string="Price")
    status = fields.Selection(selection=[("new", "New"),
            ("offerReceived", "Offer Received")], string="Status" )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property", required=True)