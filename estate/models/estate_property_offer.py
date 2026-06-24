from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description= "Estate Property Offer"

    Price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ('Accepted',"Accepted"),
            ('Refused',"refused"),
        ],
        string = "Status",
        copy = False,
    )
    partner_id = fields.Many2one('res.partner', required = True)
    property_id = fields.Many2one('estate.property', required = True)
