from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property used to buy and sell houses"

    status = fields.Char(default="New")
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(
        default=2,
    )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_accepted', "Offer Accepted"),
            ('offer_received', "Offer Received"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
            ('reset', "reset"),
        ],
        string="State",
    )

    active = fields.Boolean(default=True)

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )

    salesman_id = fields.Many2one(
        'res.users',
        string="Salesman",
        default=lambda self: self.env.user,
    )

    buyer_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        copy=False,
    )

    tag_ids = fields.Many2many(
        string="Tags",
        comodel_name='estate.property.tag',
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
        )

    total_area = fields.Float(
        compute="_compute_total_area",
        string='Total Area',
        store=True,
        help="Auto Computed field",
        )
    best_price = fields.Integer(string="Best Price", compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_price = max(rec.offer_ids.mapped("price"))
            else:
                rec.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def sold(self):
        for rec in self:
            if rec.state == "cancelled":
                message = "Property already cancelled"
                raise UserError(message)
            rec.state = "sold"
            rec.status = "Sold"

    def cancel(self):
        for rec in self:
            if rec.state == "sold":
                message = "Cannot be cancelled as its already sold"
                raise UserError(message)
            rec.state = "cancelled"
            rec.status = "Cancelled"

    def reset(self):
        for rec in self:
            if rec.state == 'sold' or rec.state == 'cancelled':
                rec.state = 'reset'
            else:
                message = "Only for sold and cancelled items "
                raise UserError(message)
