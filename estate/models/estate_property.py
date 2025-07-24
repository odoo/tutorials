from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "An Estate Property"
    _order = "id DESC"

    # Description
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection([
            ('north', "North"),
            ('west', "West"),
            ('east', "East"),
            ('south', "South"),
        ]
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection([
            ('new', "New"),
            ('received', "Offer Received"),
            ('accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default='new',
        required=True
    )
    property_type_id = fields.Many2one('property.type', string="Type")
    user_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', copy=False)
    tags_ids = fields.Many2many('property.tag', string="Tags")
    offer_ids = fields.One2many('property.offer', 'property_id', string="Offers")
    total_area = fields.Integer(compute='_compute_area')
    best_offer = fields.Float(compute='_compute_best_offer')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price>0.0)', "The expected price should be strictly positive"),
        ('check_selling_price', 'CHECK(selling_price>0)', "The selling price should be strictly positive"),
        ('check_uniq', 'UNIQUE(name)', "The name of the property should be unique")
    ]

    @api.depends('garden_area', 'living_area')
    def _compute_area(self):
        for estate in self:
            estate.total_area += estate.garden_area + estate.living_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for estate in self:
            estate.best_offer = max(estate.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_normal(self):
        for estate in self:
            if estate.state not in ['new', 'cancelled']:
                raise UserError(_("you can't delete this if state is not new or cancelled"))

    def action_set_cancelled(self):
        for estate in self:
            if estate.state == 'sold':
                raise UserError(_("Why you wanna cancel something sold fam?"))
            estate.state = 'cancelled'

    def action_set_sold(self):
        for estate in self:
            if estate.state == 'cancelled':
                raise UserError(_("you already denied the offer :'("))
            estate.state = 'sold'
