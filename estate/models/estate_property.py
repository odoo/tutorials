from odoo import fields, models


class Property(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[('new', 'New'), ('offer received', 'Offer Received'),
                   ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id=fields.Many2one("estate.property.type", string="Property Type")
    salesman = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", copy=False)
