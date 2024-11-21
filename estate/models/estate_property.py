from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"
    _order = 'id desc'
    _sql_constraints = [
        (
            'check_expected_price_strictly_positive',
            'CHECK(expected_price > 0)',
            "The expected price should be strictly positive.",
        ),
        (
            'check_selling_price_positive',
            'CHECK(selling_price >= 0)',
            "The selling price should be positive.",
        ),
    ]

    name = fields.Char("Title", required=True)

    description = fields.Text("Description")

    postcode = fields.Char("Postcode")

    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )

    expected_price = fields.Float("Expected Price", required=True)

    selling_price = fields.Float("Selling Price", readonly=True, copy=False)

    bedrooms = fields.Integer("Bedrooms", default=2)

    living_area = fields.Integer("Living Area (sqm)")

    facades = fields.Integer("Facades")

    garage = fields.Boolean("Garage")

    garden = fields.Boolean("Garden")

    garden_area = fields.Integer("Garden Area (sqm)")

    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )

    state = fields.Selection(
        string="Status",
        required=True,
        copy=False,
        default="new",
        selection=[
            ('new', "New"),
            ('received', "Offer Received"),
            ('accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
    )

    active = fields.Boolean("Active", default=True)

    property_type_id = fields.Many2one('estate.property.type', "Property Type")

    buyer_id = fields.Many2one('res.partner', "Buyer", copy=False)

    salesperson_id = fields.Many2one(
        'res.users', "Salesperson", default=lambda self: self.env.user
    )

    tag_ids = fields.Many2many('estate.property.tag')

    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    total_area = fields.Float(string="Total Area (sqm)", compute='_compute_total_area')

    best_price = fields.Float(string="Best Price", compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._("Cancelled properties cannot be sold!"))
            else:
                record.state = 'sold'
            return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._("Sold properties cannot be cancelled!"))
            else:
                record.state = 'cancelled'
            return True

    @api.constrains('selling_price')
    def _check_compare_selling_price_to_expected_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=5)
                and float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=5,
                )
                < 0
            ):
                raise ValidationError(
                    self.env._(
                        "Selling price of a property must not be less than 90 percent of the expected price."
                    )
                )
