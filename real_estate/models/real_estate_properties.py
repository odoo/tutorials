from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class real_estate(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate Property'

    name = fields.Char(default="Unknown", required=True)
    property_type_id = fields.Many2one(
        "real.estate.property.type", string="Property Type")
    street_address = fields.Char()
    description = fields.Text()
    postcode = fields.Integer()
    date_availability = fields.Datetime(default=lambda self: fields.Datetime.now() + timedelta(days=90))
    expected_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    bathrooms = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    active = fields.Boolean(default=True)
    tag_ids = fields.Many2many(
        "real.estate.tag", string="Tags", ondelete='cascade')
    offer_ids = fields.One2many(
        "real.estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total", store=True)
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        store=True)
    # ist_time = fields.Char(
    #     string="Created On (IST)",
    #     compute="_compute_create_date_ist",
    #     store=True)
    stage = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], default='new')
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False)
    selling_price = fields.Float()
    _check_expected_price_positive = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.',
    )

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for rec in self:
            if float_is_zero(rec.selling_price, precision_rounding=0.01):
                continue
            if float_compare(
                    rec.selling_price,
                    rec.expected_price * 0.9,
                    precision_rounding=0.01) < 0:
                raise ValidationError(
                    'The selling price cannot be lower than 90% of the expected price.'
                )

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_if_accepted_offer(self):
        for record in self:
            for offer in record.offer_ids:
                if offer.status == 'accepted':
                    raise UserError("Can't delete an active record!")

    # @api.depends('create_date')
    # def _compute_create_date_ist(self):
    #     for rec in self:
    #         if rec.create_date:
    #             ist_dt = fields.Datetime.context_timestamp(
    #                 rec, rec.create_date
    #             )
    #             rec.ist_time = ist_dt.strftime("%Y-%m-%d %H:%M:%S")
    #         else:
    #             rec.ist_time = False

    def action_cancel(self):
        if self.stage == 'sold':
            raise UserError("A sold property cannot be cancelled.")
        self.stage = 'cancelled'

    def action_sold(self):
        if self.stage == 'cancelled':
            raise UserError("A cancelled property cannot be sold.")
        self.stage = 'sold'
