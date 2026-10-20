from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate management module"

    name = fields.Char(string="Name", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self:fields.Date.add(fields.Date.today(), months=+3), string="Available from")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection([('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection([('new', 'New'), ('offer_received', 'Offer Receive'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancel', 'Cancelled')], default='new', copy=False, required=True)
