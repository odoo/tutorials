# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _explanation = "Represents a real estate property"
    _order = "id desc"

    name = fields.Char('Title', required=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    description = fields.Text()
    postcode = fields.Char()
    # tags =
    date_availability = fields.Date('Available From', default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    best_offer = fields.Float(compute='_compute_best_offer')
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    total_area = fields.Integer(compute='_compute_total_area')

    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ],
        required=True,
        copy=False,
        default='new')

    offer_ids = fields.One2many('estate.property.offer', inverse_name='property_id', copy=False)

    user_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)

    _check_bedrooms_not_negative = models.Constraint(
        'CHECK(bedrooms >= 0)',
        "The number of bedrooms can't be negative.",
    )

    _check_living_area_not_negative = models.Constraint(
        'CHECK(living_area >= 0)',
        "The living area can't be negative.",
    )

    _check_facades_not_negative = models.Constraint(
        'CHECK(facades >= 0)',
        "The number of facades can't be negative.",
    )

    _check_garden_area_not_negative = models.Constraint(
        'CHECK(garden_area >= 0)',
        "The garden area can't be negative.",
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max((offer.price for offer in record.offer_ids), default=None)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None
