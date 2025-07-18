from odoo import fields, models

class EstatePropertyOffer(models.Model): 
    _name = "estate.property.offer"
    _description = "Offer for a property"
    
    price = fields.Float(string="Price", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True, help="The property this offer is for")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True, help="The partner making the offer")
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False)
    