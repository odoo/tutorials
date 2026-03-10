from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property" # Removes the terminal warning

    # Required fields (not null in database)
    name = fields.Char(required=True)
    expected_price = fields.Float(required=True)

    # Basic fields
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    
    # Selection field (Dropdown)
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="The direction the garden faces."
    )