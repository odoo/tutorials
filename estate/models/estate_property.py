from odoo import models,fields

class EstateProperty(models.Model):
    _name = "estate_property"
    _description="Storing Properties of Real Estate" 

    name=fields.Char(string='property_name',required=True)
    description=fields.Text(string='property_description')
    pastcode=fields.Char(string='property_pastcode')
    date_availability =fields.Date(string='property_date_availability')
    expected_price=fields.Float(string='property_expected_price',required=True)
    selling_price=fields.Float(string='property_selling_price')
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation=fields.Selection([
        ('North','north'),
        ('South','south'),
        ('East','east'),
        ('West','west')
    ])



    






    

    
