from odoo import api, fields, models
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import _, float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"

    _order = 'id desc'

    name = fields.Char("Estate name", required=True, translate=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From", default=lambda _: date.today() + timedelta(91), copy=False
    )
    expected_price = fields.Float()
    selling_price = fields.Float("Actual Price", readonly=True)
    bedrooms = fields.Integer(default=2, copy=False)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        copy=False,
        default="new",
        required=True,
    )
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        help="Orientation of the estate property",
    )
    property_type_id = fields.Many2one('estate.property.type')
    buyer_id = fields.Many2one('res.partner')
    seller_id = fields.Many2one('res.users')
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    best_price = fields.Float(compute="_compute_best_offer")

    _check_selling_price_positive = models.Constraint(
            'CHECK(selling_price > 0)',
            'The selling price must be a positive value')

    _check_expected_price_positivie = models.Constraint(
            'CHECK(expected_price > 0)',
            "The expected price must be a postivie value")

    _check_unique_property_name = models.Constraint(
            'UNIQUE(name)',
            "The property name must be unique")

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price,
                                 precision_digits=2):
                if float_compare(record.selling_price,
                                 record.expected_price * 0.9,
                                 precision_digits=2) < 0:
                    raise ValidationError(
                            "The selling price can't be less than "
                            "90% of the expected price")

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            record.best_price = 0
            for offer in record.offer_ids:
                if record.best_price < offer.price:
                    record.best_price = offer.price

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.ondelete(at_uninstall=False)
    def _delete_check(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(_("""Cannot delete a property that received offers
                                Please first cancel the property"""))

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_("Cannot sell a cancelled property"))
            if not record.buyer_id:
                raise UserError(_("Please select a buyer before selling property"))
            record.state = 'sold'
        return True

    def action_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Cannot cancel a sold property"))
            record.state = 'cancelled'
        return True

