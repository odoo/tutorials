from odoo import models, fields


class Estate(models.Model):
    _name = "estate_property"
    _description = "Real Estate management module"

    name = fields.Char(string="Name of the property", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=(fields.Date.add(fields.Date.today(), months=+3)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('n', 'North'), ('e', 'East'), ('s', 'South'), ('w', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection([('new', 'New'), ('offer_rcv', 'Offer Receive'), ('offer_acc', 'Offer Accepted'), ('sold', 'Sold'), ('cancel', 'Cancelled')], default='new', copy=False, required=True)
