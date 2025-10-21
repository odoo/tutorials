from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"

    # FIELDS DECLARATION #
    name = fields.Char(
        string='Title',
        required=True,
        default="My new house"
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string='Available From',
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False
    )
    expected_price = fields.Float(string='Expected price', required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type")
    partner_id = fields.Many2one("res.partner", string="Buyer")
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many(
        "estate.property.offer",
        "poperty_id"
    )
