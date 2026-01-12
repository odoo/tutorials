from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False,
    )
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
        help='Garden facing direction',
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='States',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Sales Person", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if not record.mapped("offer_ids.price"):
                record.best_price = 0
            else:
                record.best_price = max(record.mapped("offer_ids.price"))

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled Properties Can Not be sold")
            if not record.buyer_id:
                raise UserError("Can not sold property who has no buyer")
            record.state = 'sold'
        return True

    def action_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold Properties can not be cancel")
            record.state = 'cancelled'
        return True

    def action_approve(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot accept other Offers.")
            target_offer = record.offer_ids.filtered(lambda r: r.price == record.best_price)
            if target_offer:
                target_offer = target_offer[0]
                target_offer.status = 'accepted'
            (record.offer_ids - target_offer).status = 'refused'
            record.selling_price = target_offer.price
            record.buyer_id = target_offer.partner_id
            record.state = 'offer_accepted'

    @api.constrains('expected_price', 'selling_price')
    def _check_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("Expected Price Must be Positive")
            if record.selling_price < 0:
                raise ValidationError("Selling price Must be Positive")

    @api.constrains('selling_price', 'expected_price')
    def _check_expected_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            expected_selling_price = record.expected_price * 0.9
            if float_compare(record.selling_price, expected_selling_price, precision_digits=2) < 0:
                raise ValidationError("Selling price Must be 90% of the expected price")
