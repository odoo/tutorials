from odoo import models, fields

class estate_property(models.Model):
    _name : "estate.property"
    _description : "estate property"

    name= fields.Char("Plan Name", default="MyName",required = True ) # required make property not nullable 
    description =  fields.Text("Plan desc")
    postcode = fields.Char('postcode')
    date_availability = fields.Date() 
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientations",
        selection=[('north', 'North'),('east','East'),('west','West'),('south','South')],
        help='this is used to select orientations of garden'
    )
    

