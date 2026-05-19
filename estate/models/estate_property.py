from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"
    _order = "id desc"

    name = fields.Char(
        string="Property Name",
        required=True,
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.today().replace(month=(fields.Date.today().month + 3) % 12),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False,
    )
    best_price = fields.Float(
        compute="_compute_best_price",
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("east", "East"), ("south", "South"), ("west", "West")],
        string="Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        string="Status",
        default="new",
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
        copy=False,
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        copy=False,
    )
    total_area = fields.Integer(
        compute="_compute_total_area",
        copy=False,
    )

    _check_expected_price = models.Constraint("CHECK (expected_price >= 0)", "The expected price must be strictly positive.")
    _check_selling_price = models.Constraint("CHECK (selling_price >=0)", "The selling price must be strictly positive.")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = min(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains("selling_price")
    def _check_minimum_selling_price(self):
        for record in self:
            if record.selling_price and float_compare(record.expected_price * 0.9, record.selling_price, precision_digits=2) > 0:
                raise ValidationError(_("The selling price must be at least 90%% of the expected price. You must reduce the expected price in order to accept this offer."))

    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_property(self):
        for record in self:
            if record.state in ("offer_received", "offer_accepted", "sold"):
                raise UserError(_("Only new or cancelled properties may be deleted."))

    def action_sold_button(self):
        if self.state != "cancelled":
            self.state = "sold"
        else:
            raise UserError(_("A cancelled property cannot be sold!"))
        return True

    def action_cancel_button(self):
        if self.state != "sold":
            self.state = "cancelled"
        else:
            raise UserError(_("A sold property cannot be cancelled!"))
        return True
