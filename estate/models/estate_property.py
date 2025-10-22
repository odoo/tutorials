from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "property data"
    notes = fields.Html()

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=date.today() + relativedelta(months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    best_offer = fields.Float(compute='_compute_best_offer', readonly=True)
    bedrooms = fields.Integer('# Bedrooms', default=2)
    living_area = fields.Integer('living area size')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('garden size')
    total_area = fields.Integer(readonly=True, compute='_compute_area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default="New"
    )
    type_id = fields.Many2one("estate.property.type", string="type")
    buyer_id = fields.Many2one("res.partner", string="buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="offer")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected_price of any property must be strictly positive.',
    )

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            prices = property.offer_ids.mapped('price')
            property.best_offer = max(prices, default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if (self.garden):
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_sold(self):
        if (self.state != "Cancelled"):
            self.state = "Sold"
        else:
            raise UserError("A cancelled property can not be sold")
        return True

    def action_cancel(self):
        if (self.state != "Sold"):
            self.state = "Cancelled"
        else:
            raise UserError("A sold property can not be cancelled")
        return True
