from odoo import fields, models
from dateutil.relativedelta import relativedelta


class propertiesPlan(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties Plan"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Datetime.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer("Bedroom", default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    buyer = fields.Char(copy=False)
    sales_person = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user and self.env.user.id or False)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Select the direction to filter the options",
        default='north'
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="Select the state of your property.",
        default='new'
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        inverse_name="property_id",
        string="Property Type"
    )
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Property Tags"
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string=""
    )
