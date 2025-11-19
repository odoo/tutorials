from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property Info"

    name = fields.Char(required=True, translate=True)
    description = fields.Text(translate=True)
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Garden_Orientation', selection=[('north', 'North'), ('east', 'East'), ('west', 'West'), ('south', 'South')])
    active = fields.Boolean(default=True)
    status = fields.Selection(required=True, copy=False, default='new', selection=[('new', 'New'), ('offer', 'Offer'), ('recieved', 'Recieved'), ('accepted', 'Accepted'), ('sold', 'Sold')])
