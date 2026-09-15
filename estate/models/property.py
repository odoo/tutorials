from odoo import models, fields


class Property(models.Model):
    _name = "estate.property"
    _description = "Real estate property"

    name = fields.Char(required=True, string='Title')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda x: fields.Date.add(fields.Date.today(), months=3),
                                    string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    faces = fields.Integer(string="Facade")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=(('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')))
    active = fields.Boolean(default=True)
    state = fields.Selection(default='new', required=True, copy=False,
                             selection=(('new', 'New'), ('offer_received', 'Offer Received'),
                                        ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                        ('cancelled', 'Cancelled')))
