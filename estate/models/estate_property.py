from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Property Name", required=True)
    reference = fields.Char(string="Reference")
    description = fields.Text(string="Description")

    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price")

    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Float(string="Living Area (sqm)")
    garden_area = fields.Float(string="Garden Area (sqm)")

    garden = fields.Boolean(string="Garden")
    garage = fields.Boolean(string="Garage")

    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default="new")

    active = fields.Boolean(default=True)
