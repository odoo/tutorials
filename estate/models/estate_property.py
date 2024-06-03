# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate_property'  # change _ to .
    _description = 'Real Estate Property'
    _order = 'id desc'

    def _in_three_months(self):
        self.date_availability = fields.date.today()
        return fields.date.today() + fields.date_utils.relativedelta(months=3)

    def _default_salesperson(self):
        return self.env.user

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=_in_three_months,
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
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
        ('west', 'West'),
    ])

    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], default='new', copy=False, string="Status")

    property_type_id = fields.Many2one(
        'estate_property_type',
        string='Property Type'
    )
    buyer = fields.Many2one('res.partner', copy=False)
    salesperson = fields.Many2one('res.users', default=_default_salesperson)
    offers_ids = fields.One2many('estate_property_offer', 'property_id')
    tag_ids = fields.Many2many('estate_property_tags')

    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offers_ids.price')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.offers_ids.mapped('price') or [0.0])

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.onchange('date_availability')
    def _onchange_date_availability(self):
        if self.date_availability and self.date_availability < fields.date.today():
            return {"warning": {
                "title": "Warning",
                "message": "Available    date must be greater than current date",
            }
            }

    def action_set_sold_property(self):
        if self.state == "canceled":
            raise UserError("You cannot set a canceled property to sold")

        self.state = 'sold'

    def action_set_canceled_property(self):
        if self.state == "sold":
            raise UserError("You cannot set a sold property to canceled")

        self.state = 'canceled'

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0.0)", "The expected price must be positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The selling price must be positive"),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for rec in self:
            ninety_percent_expected_price = rec.expected_price * 0.9
            if rec.selling_price < ninety_percent_expected_price and rec.selling_price != 0.0:
                rec.selling_price = None
                rec.buyer = None
                raise ValidationError('The selling price cannot be lower than 90% of the expected price')

    @api.ondelete(at_uninstall=False)
    def unlink_check(self):
        """
        Prevent deletion of properties that are not in 'new' or 'canceled' state
        """
        if self.state != 'new' and self.state != 'canceled':
            raise UserError(_('You cannot delete a property that is not new or canceled.'))

        return super().unlink()


