from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "estate property used to buy and sell houses"
    _log_access = False

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    bedrooms = fields.Integer(default=2)
    date_availability = fields.Date(
        default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3),
        copy=False
    )
    description = fields.Text()
    expected_price = fields.Float(required=True)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )
    living_area = fields.Integer()
    postcode = fields.Char()
    property_type_id = fields.Many2one('estate.property.type')
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', copy=False)
    selling_price = fields.Float(readonly=True, copy=False)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default='new',
        copy=False,
        required=True,
    )
    tag_ids = fields.Many2many('estate.property.tag')
