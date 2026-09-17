from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstatePropertyModel(models.Model):
    _name = "estate_property"
    _description = "The details of a property"

    name = fields.Char('Estate Name', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    has_garage = fields.Boolean()
    has_garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
           ('east', 'East'),
           ('west', 'West'),
           ('north', 'North'),
           ('south', 'South'),
        ],
    )
    state = fields.Selection(
        string='State',
        selection=[
           ('new', 'New'),
           ('offer_received', 'Offer Received'),
           ('offer_accepted', 'Offer Accepted'),
           ('sold', 'Sold'),
           ('cancelled', 'Cancelled'),
        ],
        default='new',
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate_property_type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    property_tags_ids = fields.Many2many("estate_property_tag", string="Tags")
    offers_ids = fields.One2many("estate_property_offer", "property_id", string="Offers")
