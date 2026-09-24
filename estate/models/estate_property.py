from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import float_compare
from odoo.tools.float_utils import float_is_zero


class Property(models.Model):
    _name = "estate_property"
    _description = "estate property model"
    _order = "id desc"

    name = fields.Char('Nom', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Date Availability', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Prince', readonly=True, copy=False)
    bedrooms = fields.Integer('# Bedrooms', default=2)
    living_area = fields.Integer('# Living Areas')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean('Has Garage')
    garden = fields.Boolean('Has Garden')
    garden_area = fields.Integer('# Garden Areas')
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
        ('north', "North"),
        ('south', "South"),
        ('east', "East"),
        ('west', "West"),
        ]
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default='new',
    )

    salesperson = fields.Many2one('res.users', string="Salesperson", index=True, default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string="Buyer", copy=False)

    tag_ids = fields.Many2many('estate_property.tag', string="Tags")

    offer_ids = fields.One2many('estate_property.offer', 'property_id', string="Offer")

    total_area = fields.Integer(compute="_compute_areas")

    best_price = fields.Float(compute="_compute_best_price")

    property_type_id = fields.Many2one(
        "estate_property.type",
        string="Property Type",
    )

    @api.depends('description', 'garden_area')
    def _compute_areas(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids.mapped("price") else 0

    @api.onchange('garden')
    def on_change_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def sold_property_action(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled property cannot be sold")
            elif record.state == 'sold':
                raise UserError("The Property was sold already")
            record.state = 'sold'
        return True

    def cancel_property_action(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold property cannot be cancelled")
            elif record.state == 'cancelled':
                raise UserError("The Property was already cancelled")
            record.state = 'cancelled'
        return True

    def accept_property_offer_action(self, buyer, price):
        for record in self:
            if record.buyer:
                raise UserError("Property has already been sold")
            record.buyer = buyer
            record.selling_price = price
            record.state = 'offer_accepted'
        return True

    _check_expected_price = models.Constraint(
        'CHECK(expected_price >0)',
        'The Expected Price should be strictly positive'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The Selling Price Should be positive'
    )

    @api.constrains('selling_price')
    def check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2):
                if float_compare(record.selling_price * 0.9, record.expected_price, 2) == -1:
                    raise UserError("The Selling Price cannot be lower than 90 percent of the Expected Price")
