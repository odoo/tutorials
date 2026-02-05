from odoo import fields, models


class RealEstateProperty(models.Model):

    _name = "estate.property"
    

    _description = "Real Estate Properties"
    
    name = fields.Char(
        string="Property Name", 
        required=True,           
        help="Enter the name/title of the property"
    )
    
