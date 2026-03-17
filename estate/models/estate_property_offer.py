from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"


    price = fields.Char(required = True)
    status = fields.Selection(
         selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ]
        , copy= False 
    )

    partner_id = fields.Many2one('res.partner' , "Partner")
    property_id = fields.Many2one('estate.property' , "Property")