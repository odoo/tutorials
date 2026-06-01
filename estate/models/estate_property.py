from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstatePropery(models.Model):
    _name = 'estate.property'
    _description = "Estate property"
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: self.__default_date_availability(),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ('north', "North"),
            ('east', "East"),
            ('south', "South"),
            ('west', "West"),
        ],
    )
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')
    property_type_id = fields.Many2one('estate.property.type')
    tag_ids = fields.Many2many('estate.property.tag')
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        copy=False,
        default='new',
    )

    _expected_price_constraint = models.Constraint(
        'CHECK(expected_price >= 0)',
        "Expected price must be positive.",
    )
    _selling_price_constraint = models.Constraint(
        'CHECK(selling_price >= 0)',
        "Selling price must be positive.",
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0)

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_and_expected_price(self):
        for property in self:
            if (
                not float_is_zero(property.selling_price, 0)
                and float_compare(
                    property.expected_price * 0.9,
                    property.selling_price,
                    0,
                )
                > 0
            ):
                raise ValidationError(
                    _(
                        "You cannot accept an offer lower than 90% of the expected price. Lower the expected price if you want to accept it.",
                    ),
                )

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_except_valid_state(self):
        if any(property.state not in ['new', 'cancelled'] for property in self):
            raise UserError(
                _("Can't delete a property if status is not New or Cancelled"),
            )

    def action_cancel_property(self):
        for property in self:
            if property.state == 'sold':
                raise UserError(_("Sold properties cannot be cancelled."))
            property.state = 'cancelled'

    def action_mark_sold_property(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError(_("Cancelled properties cannot be sold."))

            if not any(offer.status == 'accepted' for offer in property.offer_ids):
                raise UserError(
                    _("Properties without an accepted offer cannot be marked sold."),
                )

            property.state = 'sold'

    def __default_date_availability(self):
        return datetime.today() + relativedelta(months=3)
