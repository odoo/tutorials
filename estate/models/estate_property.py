from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Management"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    active = fields.Boolean(default=True)
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3), string="Available from")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    state = fields.Selection(
        string="State",
        selection=[('new', 'New Offer Received'), ('offer', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        default='new'
    )