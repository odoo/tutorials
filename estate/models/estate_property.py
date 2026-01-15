from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Module"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
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
      ('cancelled', 'Cancelled'),
      ],
      required=True, copy=False, default='new', string="Status")
    property_type_id = fields.Many2one('estate_property_type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default = lambda self: self.env.user)
    tag_ids = fields.Many2many('estate_property_tag', string="Property Tags")
    offer_ids = fields.One2many('estate_property_offer', 'property_id', string="Offers")
    total_area = fields.Float("Total Area (sqm)", compute='_compute_total_area')
    best_price = fields.Float("Best Offer", compute="_compute_best_offer")

    _check_expected_price_strictly_positive = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price should be strictly positive.',
    )

    _check_selling_price_positive = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price should be positive.',
    )

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price_90_percent_expected_price(self):
        for record in self:
            if (record.selling_price > 0) and ((100 / record.expected_price * record.selling_price) < 90):
                raise ValidationError("The selling price cannot be lower than 90 % from expected price")
        # all records passed the test, don't return anything

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
      for record in self:
          record.best_price = max(self.offer_ids.mapped('price')) if self.offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_sold(self):
        _logger.info("SOLD")
        for record in self:
            if record.state == "cancelled":
                raise UserError("Canceled properties cannot be sold.")
            return self.write({'state': 'sold'})

    def action_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be canceled.")
            return self.write({'state': 'cancelled'})

    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_new_or_cancelled(self):
        _logger.warning("ON_DELETE")
        if any((record.state not in ('new', 'cancelled')) for record in self):
            raise UserError("Only new and canceled properties can be deleted.")
