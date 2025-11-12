# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Properties"
    _order = 'id desc'
    _sql_constraints = [
        ('check_expected_price', "CHECK(expected_price > 0)",
        "The expected price must be strictly positive"),
        ('check_selling_price', "CHECK(selling_price >= 0)",
        "The selling price must be positive"),
    ]

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    image = fields.Binary(string="Property Image")
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        default=lambda self:fields.Date.add(fields.Date.today(), months=3),
        copy=False
        )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(index=True, default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        copy=False
    )
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string="Property Type")
    buyer_id = fields.Many2one(comodel_name='res.partner', string="Buyer", copy=False)
    salesman_id = fields.Many2one(comodel_name='res.users', string="Salesman", default=lambda self:self.env.uid)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="offer_id")
    total_area = fields.Integer(compute='_compute_total_area', string="Total Area (sqm)")
    best_offer = fields.Float(compute='_compute_best_offer', string="Best Offer", store=True)
    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self:self.env.company)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            if property.offer_ids:
                property.best_offer = max(property.offer_ids.mapped('price'))
            else:
                property.best_offer = 0.0

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            if not float_is_zero(property.selling_price, precision_rounding=0.01):
                if property.selling_price < property.expected_price * 0.9:
                    raise ValidationError("Offer price can't be less than 90% of expected price")

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _restrict_property_unlink(self):
        for property in self:
            if property.state not in ['new', 'cancelled']:
                raise UserError(_("Can't delete a sold property or with an offer."))

    def action_sold(self):
        for property in self:
            if property.offer_ids:
                rc = property.offer_ids.mapped('status')
                if not any(status=='accepted' for status in rc) or not rc:
                    raise ValidationError(_("One of the offer(s) must be accepted before selling property."))
            else:
                raise UserError(_("Can't sell a property without offer."))
            if property.state == 'cancelled':
                raise UserError(_("cancelled properties can't be sold"))
            else:
                for property in self:
                    property.state = 'sold'

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError(_("sold properties can't be cancelled"))
            else:
                for property in self:
                    property.state = 'cancelled'

    def check_offer(self):
        for property in self:
            if property.state=="new" and property.offer_ids:
                property.state='Offer Received'
                return property
