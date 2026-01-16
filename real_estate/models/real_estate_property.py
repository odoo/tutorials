from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class real_estate(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate Property'
    _order = "id desc"

    name = fields.Char(required=True)
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
    maintenance_request_ids = fields.One2many(
        "real.estate.property.maintenance.request", "property_id", string="Maintenance Requests")
    total_maintenance_cost = fields.Float(compute="_compute_total_maintenance_cost", store=True, string="Total Cost")
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson'
    )
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
                    'The selling price cannot be lower than 90% of the expected price.')

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = []
            for offer in record.offer_ids:
                prices.append(offer.price)
            record.best_price = max(prices) if prices else 0.0

    @api.depends('maintenance_request_ids.cost')
    def _compute_total_maintenance_cost(self):
        for record in self:
            costs = record.maintenance_request_ids.mapped('cost')
            record.total_maintenance_cost = sum(costs) if costs else 0.0

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
    def _check_property_delete(self):
        for record in self:
            if record.stage not in ('new', 'cancelled'):
                raise UserError(
                    "You can only delete properties in New or Cancelled state."
                )

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
        maintenace_request = self.maintenance_request_ids.filtered_domain([('status', '!=', 'done')])
        if maintenace_request:
            raise UserError("CProperty cannot be sold , there is any maintenance request not done")
        self.stage = 'sold'

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for rec in self:
            if rec.expected_price < 0:
                raise ValidationError(
                    'The selling price cannot be lower than 90% of the expected price.'
                )
