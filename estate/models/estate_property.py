from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "reals estate properties"

    name = fields.Char('Property Name',required=True)
    description = fields.Text('The Descritption')
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area= fields.Integer()
    garden_orientation = fields.Selection([("North","North"),("South","South"),("East","East"),("West","West")])

