from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        string="Available From", copy=False,
    )
    expected_price = fields.Float(string="Property Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('received', "Offer Received"),
            ('accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ], required=True, copy=False, default='new',
    )
    buyer_id = fields.Many2one("res.partner")
    salesman_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    type_id = fields.Many2one("estate.property.type", string="Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id',
                                string="Offers")

    total_area = fields.Float(string="Total Area", compute="_compute_total_area",
                              store=True)

    best_price = fields.Float(string="Best price",
                              compute='_compute_best_price', store=True)

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for val in self:
            val.total_area = val.living_area + val.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for val in self:
            val.best_price = max(val.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False
