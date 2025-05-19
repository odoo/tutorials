from odoo import fields, models

class Estate_property(models.Model):
    _name = "estate.property"
    _description = "Model to modelize Real Estate objects"

    name = fields.Char(required=True)
    description  = fields.Text()
    postcode = fields.Char()
    date_availabilty = fields.Datetime()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north','North'), ('south','South'),('east','East'),('west','West')],
        help="Orientation is meant to describe the garden"
    )
