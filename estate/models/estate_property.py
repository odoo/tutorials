from odoo import fields,models

class EstateProperty(models.model):
    _name ='estate.property'
    _description='Real Estate Property'

   # Basic fields for property details
    name = fields.Char(string="Property Name", required=True) 
    description = fields.Text(string="Description")  
    postcode = fields.Char(string="Postcode") 
    date_availability = fields.Date(string="Availability Date") 
    expected_price = fields.Float(string="Expected Price", required=True)  
    selling_price = fields.Float(string="Selling Price")  
    bedrooms = fields.Integer(string="Bedrooms")  
    living_area = fields.Integer(string="Living Area (sq.m.)")  
    facades = fields.Integer(string="Number of Facades")  
    garage = fields.Boolean(string="Has Garage")  
    garden = fields.Boolean(string="Has Garden")  
    garden_area = fields.Integer(string="Garden Area (sq.m.)")
    garden_orientation=fields.Selection([('north','North'),('south','South'),('east','East'),('west','West')],String='Garden Orientation')  
    