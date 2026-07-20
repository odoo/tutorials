from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.',
    )
    _check_positive_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive.',
    )

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )
    maintenance_ids = fields.One2many(
        "estate.property.maintenance",
        "property_id",
        string="Maintenance",
    )
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Datetime.now() + timedelta(days=90),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(
        default=2,
    )
    facades = fields.Integer()
    garage = fields.Boolean()
    living_area = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(
        compute="_compute_total_area",
    )
    best_price = fields.Float(
        compute="_compute_best_price",
    )
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(
        default=True,
    )
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
        default='new',
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = (
                property.living_area +
                property.garden_area
            )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            prices = property.offer_ids.mapped("price")
            property.best_price = max(prices) if prices else 0.0

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for property in self:
            if property.selling_price == 0:
                continue
            minimum_price = property.expected_price * 0.9
            if property.selling_price < minimum_price:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=True)
    def _unlink_if_state_new_cancelled(self):
        for property in self:
            if property.state in ('offer_received', 'offer_accepted', 'sold'):
                raise UserError(
                    "Only new & cancelled properties can be deleted."
                )

    def action_sold(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError(
                    "Cancelled properties cannot be sold."
                )
            property.state = "sold"
        return True

    def action_cancel(self):
        for property in self:
            if property.state == "sold":
                raise UserError(
                    "Sold properties cannot be cancelled."
                )
            property.state = "cancelled"    
        return True
