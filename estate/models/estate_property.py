from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import _, api, exceptions, fields, models
from odoo.tools import float_utils


class EstateProperty(models.Model):
    # ----------------------------------------
    # Private attributes
    # ----------------------------------------
    _name = 'estate.property'
    _description = "Comprehensive platform for managing properties, sales, rentals, and client relationships throughout their entire lifecycle."
    _sql_constraints = [
        (
            'check_expected_price_positive',
            'CHECK (expected_price > 0)',
            "Expected price must be positive.",
        ),
        (
            'check_selling_price_positive',
            'CHECK (selling_price >= 0)',
            "Selling price must be positive.",
        ),
    ]
    _order = 'id desc'

    # ----------------------------------------
    # Field declarations
    # ----------------------------------------
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: date.today() + relativedelta(months=3)
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
        string="Garden Orientation",
        selection=[
            ('n', "North"),
            ('s', "South"),
            ('e', "East"),
            ('w', "West"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default='new',
        required=True,
        copy=False,
    )
    buyer_id = fields.Many2one(
        'res.partner', string="Buyer", index=True, copy=False
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        index=True,
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    total_area = fields.Float(
        compute="_compute_total_area"
    )
    best_price = fields.Float(
        compute="_compute_best_price", readonly=True
    )

    # ----------------------------------------
    # Compute, inverse and search methods
    # ----------------------------------------
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for estate in self:
            estate.best_price = max(
                estate.offer_ids.mapped('price'), default=0.0
            )

    # ----------------------------------------
    # Constrains and onchange methods
    # ----------------------------------------
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for estate in self:
            if (
                estate.selling_price != 0
                and float_utils.float_compare(
                    estate.selling_price,
                    estate.expected_price * 0.9,
                    precision_digits=2,
                )
                < 0
            ):
                raise exceptions.ValidationError(
                    _(
                        "Selling price must be greater than or equal to 90% of expected price."
                    )
                )

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            if not self.garden_area:
                self.garden_area = 10
            if not self.garden_orientation:
                self.garden_orientation = 's'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # ----------------------------------------
    # CRUD methods (ORM overrides)
    # ----------------------------------------
    @api.ondelete(at_uninstall=False)
    def _unlink_if_user_new_cancelled(self):
        for estate in self:
            if estate.state not in ['new', 'cancelled']:
                raise exceptions.UserError(
                    _("Can't delete an active property!")
                )

    # ----------------------------------------
    # Action methods
    # ----------------------------------------
    def action_sold_property(self):
        for estate in self:
            if estate.state == 'cancelled':
                raise exceptions.UserError(_("Cannot set as sold if cancelled"))
            estate.state = 'sold'
            # Set buyer from accepted offer
            accepted_offer = estate.offer_ids.filtered(
                lambda o: o.status == 'accepted'
            )
            if accepted_offer:
                estate.buyer_id = accepted_offer.partner_id
                # Ensure selling price is set from the accepted offer
                if not estate.selling_price:
                    estate.selling_price = accepted_offer.price
        return True

    def action_cancel_property(self):
        for estate in self:
            if estate.state == 'sold':
                raise exceptions.UserError(_("Cannot cancel if already sold"))
            estate.state = 'cancelled'
        return True
