from datetime import datetime, timedelta

from odoo.exceptions import UserError
from odoo import api, exceptions, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: datetime.now() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling price must be positive.'),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.expected_price and record.selling_price < 0.9 * record.expected_price:
                raise exceptions.ValidationError("Selling price cannot be lower than 90% of the expected price.")

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'), 
        ('east', 'East'),
        ('west', 'West')
    ],
        help="Orientation of Garden")

    @api.onchange()
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    total_area = fields.Float(compute="_compute_total_area", string="Total Area")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    best_price = fields.Float(compute="_compute_best_price", string="Best Offer", store=True)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')],
        required=True, default='new')

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("You cannot cancel a sold property.")
            record.state = 'canceled'

    def action_set_sold_property(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("You cannot sell a cancelled property.")
            record.state = 'sold'

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    seller_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_cancelled(self):
        for property in self:
            if property.state not in ['new', 'cancelled']:
                raise UserError('You cannot delete a property unless it is in "New" or "Cancelled" state.')
