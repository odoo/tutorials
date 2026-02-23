from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    #
    # Default methods
    #
    def _default_available_from(self):
        return fields.Date.today() + relativedelta(months=3)

    #
    # Fields declaration
    #
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()

    available_from = fields.Date(
        copy=False,
        default=_default_available_from
    )

    expected_price = fields.Float(
        required=True,
        digits=(12, 2)
    )

    selling_price = fields.Float(
        readonly=True,
        copy=False,
        digits=(12, 2)
    )

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")

    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )

    active = fields.Boolean(default=True)

    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new'
    )

    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type'
    )

    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False
    )

    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user
    )

    tag_ids = fields.Many2many(
        'estate.property.tag',
        string="Tags"
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string="Offers"
    )

    total_area = fields.Float(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        store=True
    )

    best_offer = fields.Float(
        string="Best Offer",
        compute="_compute_best_offer",
        store=True
    )

    #
    # SQL constraints
    #
    _sql_constraints = [
        (
            'expected_price_positive',
            'CHECK(expected_price > 0)',
            "The expected price must be strictly positive.",
        ),
        (
            'selling_price_positive',
            'CHECK(selling_price >= 0)',
            "The selling price cannot be negative.",
        ),
    ]

    #
    # Compute methods
    #
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for prop in self:
            prop.best_offer = max(prop.offer_ids.mapped('price'), default=0)

    #
    # Selection methods (if any)
    #
    # (none in this model)

    #
    # Onchange methods
    #
    @api.onchange('garden')
    def _onchange_garden(self):
        for prop in self:
            if prop.garden:
                prop.garden_area = 10
                prop.garden_orientation = 'north'
            else:
                prop.garden_area = 0
                prop.garden_orientation = False

    #
    # Constraint methods
    #
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_min(self):
        for prop in self:
            if not prop.selling_price or not prop.expected_price:
                continue
            if float_compare(
                prop.selling_price,
                prop.expected_price * 0.9,
                precision_digits=2
            ) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% "
                    "of the expected price."
                )

    #
    # CRUD overrides
    #
    @api.ondelete(at_uninstall=False)
    def _check_can_delete(self):
        for prop in self:
            if prop.state not in ('new', 'cancelled'):
                raise UserError(
                    "Only properties in 'New' or 'Cancelled' state "
                    "can be deleted."
                )

    #
    # Action methods
    #
    def action_cancel(self):
        self.ensure_one()
        if self.state == 'sold':
            raise UserError("Sold properties cannot be cancelled.")
        self.state = 'cancelled'
        return True

    def action_sold(self):
        self.ensure_one()
        if self.state == 'cancelled':
            raise UserError("Cancelled properties cannot be sold.")
        self.state = 'sold'
        return True
