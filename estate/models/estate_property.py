import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)',
         'The expected price should be positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price should be positive'),
    ]

    name = fields.Char(
        required=True,
        string="Title",
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.today() + datetime.timedelta(days=92),
        string="Available From",
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        readonly=False,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for estate in self:
            estate.best_price = max(estate.offer_ids.mapped("price") + [0])

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def sold_property(self):
        for estate in self:
            if estate.state != "canceled":
                estate.state = "sold"
            else:
                raise UserError(_("Canceled properties cannot be sold."))
        return True

    def cancel_property(self):
        for estate in self:
            if estate.state != "sold":
                estate.state = "canceled"
            else:
                raise UserError(_("Sold properties cannot be canceled."))
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if (
                    not float_is_zero(record.selling_price, 0)
                    and float_compare(record.selling_price, 0.9 * record.expected_price, 1) == -1
            ):
                raise ValidationError(_("The selling price must be at least 90% of the expected price"))

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        for estate in self:
            if estate.state not in ("new", "canceled"):
                raise UserError(_("Only canceled or new properties can be deleted."))
