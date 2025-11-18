from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties"


    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Property Description', required=True)
    postcode = fields.Char('Property postcode')
    date_availability = fields.Date('Property availability date')
    expected_price = fields.Float('Property expected price')
    selling_price = fields.Float('Property selling price')
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'), ('east','East'), ('west', 'West')])

