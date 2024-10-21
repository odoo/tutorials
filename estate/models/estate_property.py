from odoo import fields, models, tools, api
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char("Name of the Property", required=True)
    description = fields.Char("Description")
    postcode = fields.Char("Postcode")
    expected_price = fields.Float("Expected Price", required=True, default=1)
    date_availability = fields.Date(
        "Available From",
        default=tools.date_utils.add(fields.Date.today(), months=3),
        copy=False
    )
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price", string="Best offer price")
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garden = fields.Boolean("Garden")
    garage = fields.Boolean("Garage")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("east", "East"),
            ("south", "South"),
            ("west", "West")
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean("Available", default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        required=True,
        copy=False,
        default="new",
        string="State"
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_area, self.garden_orientation = "10", "north"
        else:
            self.garden_area, self.garden_orientation = "0", ""

    def set_property_to_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError('Cancelled properties cannot be sold')

            if record.selling_price == 0:
                raise UserError('A property cannot be sold for 0€, accept an offer before selling a property')
            record.state = "sold"
        return True

    def set_property_to_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError('Sold properties cannot be cancelled')
            record.state = "cancelled"
        return True

    _sql_constraints = [
        (
            'check_expected_price',
            'CHECK(expected_price > 0)',
            'The expected price of a propery should always be positive'
        ),
        (
            'check_selling_price',
            'CHECK(selling_price >= 0)',
            'The selling price of a propery should always be positive'
        )
    ]

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not tools.float_utils.float_is_zero(record.selling_price, precision_rounding=0.01) \
                and tools.float_utils.float_compare(record.selling_price, 0.9 * record.expected_price, precision_rounding=0.01) < 0:
                raise ValidationError('The selling price must be at least 90% of the expected price.')

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_cancelled(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError('Impossible to delete a properrty that is not new or cancelled')
