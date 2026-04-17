from odoo import api, fields, models
from odoo.tools import date_utils
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property for purchasing and selling properties"

    name = fields.Char(required=True, string="Property Name")
    description = fields.Char()
    postcode = fields.Char()
    date_availibility = fields.Date(copy=False, default=lambda x: fields.Date.today() + date_utils.get_timedelta(3, "month"))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),

        ],
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer received'),
            ('offer accepted', 'Offer accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type Id")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    salesperson = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    active = fields.Boolean()

    total = fields.Integer(compute='_compute_totalArea')
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_totalArea(self):
        for record in self:
            record.total = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            if prices:
                record.best_price = max(prices)
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold_property(self):
        if self.state == 'cancelled':
            raise UserError("A cancelled property cannot be set as sold.")
            return False

        self.state = 'sold'
        return True

    def action_cancel_property(self):
        if self.state == 'sold':
            raise UserError("A sold property cannot be set as cancelled.")

        self.state = 'cancelled'
        return True
