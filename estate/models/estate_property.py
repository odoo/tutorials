from odoo import _, api, fields, exceptions, models
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "Properties of the Estate app"

    _sql_constraints = [
        (
            "positive_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price should be strictly positive.",
        ),
        (
            "positive_selling_price",
            "CHECK(selling_price > 0)",
            "The selling price should be strictly positive",
        ),
    ]
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda _: fields.Date.add(fields.Date.today(), months=3),
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
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one('estate.property.type', "Type")
    salesman_id = fields.Many2one(
        'res.users',
        "Salesman",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one('res.partner', "Buyer", copy=False)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', "Offers")
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        self.best_price = max(self.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def sold_property_button_action(self):
        for record in self:
            if self.state != 'cancelled':
                record.state = 'sold'
            else:
                error_msg = _("Cannot set cancelled property as sold.")
                raise exceptions.UserError(error_msg)

    def cancel_property_button_action(self):
        for record in self:
            if self.state != 'sold':
                record.state = "cancelled"
            else:
                error_msg = _("Cannot set sold property as cancelled.")
                raise exceptions.UserError(error_msg)

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_90_perc(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if (
                float_compare(
                    record.selling_price,
                    0.9 * record.expected_price,
                    precision_digits=2,
                )
                == -1
            ):
                error_msg = _(
                    "The selling price must be at least 90% of the expected price."
                )
                raise exceptions.ValidationError(error_msg)

    @api.ondelete(at_uninstall=False)
    def avoid_forbidden_deletion(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                error_msg = _(
                    "Cannot cancel records not in the New or Cancelled stage."
                )
                raise exceptions.UserError(error_msg)
