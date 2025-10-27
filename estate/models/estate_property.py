from odoo import models,fields

class estateproperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required='True')
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')],
        string="Garden Orientation"
    )
    active = fields.Boolean(string="Active", default=True)