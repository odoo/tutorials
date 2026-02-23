from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Test Model for real estate"

    name = fields.Char(default="Unknown")
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float()
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    state = fields.Selection(
        string="status",
        selection=[
            ('new', "New"),
            ('offer received', "Offer Received"),
            ('offer accepted', "Offer Accepted"),
            ('sol', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default='new',
    )
    active = fields.Boolean(default=True)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="garden orientation direction",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )
    property_type_id = fields.Many2one("estate.property.type")
