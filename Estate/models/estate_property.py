from odoo import models, fields
from datetime import date, timedelta


class Testing(models.Model):
    _name = "estate.property"
    _description = "This is Real Estate"

    name = fields.Char('property_Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date_avail', copy=False, default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float('exp_price', required=True)
    selling_price = fields.Float('sell_price', readonly=True, copy=False)
    bedrooms = fields.Integer('bedrooms', default=2)
    living_area = fields.Integer('live_area')
    facades = fields.Integer('facades')
    garage = fields.Boolean('garage')
    garden = fields.Boolean('garden')
    garden_area = fields.Integer('garden_area')
    garden_orientation = fields.Selection(
        string='Garden direction',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    state = fields.Selection(
        string='state',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        default='new',
        copy=False
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        inverse_name="property_id",
        string="property name"
    )
    salesperson_id = fields.Many2one("res.users", string="Sales person", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="property offer")
