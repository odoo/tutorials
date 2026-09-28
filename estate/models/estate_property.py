from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate property informations"
    _order = 'id desc'

    currency_id = fields.Many2one(
        "res.currency", string="Currency",
        default=lambda self: self.env.company.currency_id,
    )
    name = fields.Char(required=True, string="Title")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(copy=False, default=lambda x: fields.Date.add(fields.Date.today(), months=3), string="Available From")
    expected_price = fields.Monetary(required=True, string="Expected Price")
    selling_price = fields.Monetary(readonly=True, copy=False, string="Selling Price")
    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        help="Orientation precises where the garden is oriented"
    )
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        default='new',
    )
    active = fields.Boolean(default=True, string="Active")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers", copy=False)
    total_area = fields.Float(compute='_compute_total_area', string="Total Area (sqm)")
    best_price = fields.Monetary(compute='_compute_best_price', string="Best Price")

    _check_positive_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        "The expected price should be positive."
    )

    _check_positive_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        "The selling price should be positive."
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.currency_id.compare_amounts(record.selling_price, record.expected_price * 0.9) <= 0 and not record.currency_id.is_zero(record.selling_price):
                raise ValidationError(r"The selling price must be at least 90 % of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        if any(record.state for record in self if record.state not in ('new', 'cancelled')):
            raise UserError(self.env._("You should not delete properties that are not new or cancelled."))

    def sell_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._("Cancelled properties cannot be sold."))
            record.state = 'sold'
        return True

    def cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._("Sold properties cannot be cancelled."))
            record.state = 'cancelled'
        return True
