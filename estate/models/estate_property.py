from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    _order = 'id desc'

    # fields
    name = fields.Char('Name', required=True)
    expected_price = fields.Float('Expected Price', digits=(12, 2), required=True)
    description = fields.Char('Description')
    date_availability = fields.Date('Available From', default=lambda self: fields.Date.add(fields.Date.today(), months=3), copy=False)
    selling_price = fields.Float('Selling Price', digits=(12, 2), readonly=True, copy=False)
    postcode = fields.Char('Postcode')
    bedrooms = fields.Integer('Bedrooms', default=2)
    facades = fields.Integer('Facades')
    living_area = fields.Integer('Living area')
    garden_area = fields.Integer('Garden area')
    total_area = fields.Integer(string='Total Area', compute='_compute_total', store=True)
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
        )
    garage = fields.Boolean('Has a Garage')
    garden = fields.Boolean('Has a Garden')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[("new", "New"), ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        required=True,
        default="new",
        copy=False
    )
    best_price = fields.Float('Best Offer', digits=(12, 2), compute='_compute_best_price', store=True)
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")

    # sql constraints
    _check_living_area = models.Constraint(
        "CHECK(living_area >= 0)",
        "The living area surface has to be positive."
    )
    _check_garden_area = models.Constraint(
        "CHECK(garden_area >= 0)",
        "The garden area surface has to be positive."
    )
    _check_bedrooms = models.Constraint(
        "CHECK(bedrooms >= 0)",
        "The bedroom number has to be positive."
    )
    _check_facades = models.Constraint(
        "CHECK(facades > 0)",
        "The facade number has to be positive."
    )
    _check_expected_price_positive = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price has to be strictly positive"
    )
    _check_selling_price_positive = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price has to be positive."
    )

    # computed methods
    @api.depends('garden_area', 'living_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids', 'offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    # contraints / onchange
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=2)
                and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0
                ):
                raise ValidationError(self.env._('The selling price has to be min. 90% of the expected price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False

    # crud
    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_new_or_cancel(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(self.env._('Only new or cancelled properties can be deleted'))
        record.offer_ids.unlink()

    # actions
    def action_property_cancelled(self):
        for record in self:
            if record.state == ['sold', 'cancelled']:
                raise UserError(self.env._('A sold (or cancelled) property can\'t be cancelled'))
            record.state = "cancelled"
            record.selling_price = 0
            record.buyer_id = False
            record.offer_ids.status = False

    def action_property_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._('A cancelled property can\'t be sold'))
            record.state = "sold"

    # business methods
