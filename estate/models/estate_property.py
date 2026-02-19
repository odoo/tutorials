from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()

    available_from = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3)
    )

    expected_price = fields.Float(required=True)

    selling_price = fields.Float(
        readonly=True,
        copy=False
    )

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")

    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )

    # Constraints and Onchange methods
    @api.onchange('garden')
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_area = 10
                property.garden_orientation = 'north'
            else:
                property.garden_area = 0
                property.garden_orientation = False

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
    # Many2one links
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
    # Many2many links
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string="Tags"
    )

    # One2many links
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string="Offers"
    )

    # Computed Fields
    total_area = fields.Float(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        store=True
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    best_offer = fields.Float(
        string="Best Offer",
        compute="_compute_best_offer",
        store=True
    )

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped('price'), default=0)

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            property.state = 'cancelled'
        return True

    def action_sold(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            property.state = 'sold'
        return True

    _check_selling_price_min = models.Constraint(
        """
        CHECK(
            selling_price > 0
            OR selling_price >= expected_price * 0.9
        )
        """,
        "The selling price cannot be lower than 90% of the expected price.",
    )

    _check_expected_price_positive = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )

    _check_selling_price_positive = models.Constraint(
        "CHECK(selling_price > 0)",
        "The selling price cannot be negative.",
    )

    @api.ondelete(at_uninstall=False)
    def _check_can_delete(self):
        for prop in self:
            if prop.state not in ('new', 'cancelled'):
                raise UserError("Only properties in 'New' or 'Cancelled' state can be deleted.")
