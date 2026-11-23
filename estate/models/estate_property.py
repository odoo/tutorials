from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="new",
        copy=False,
        compute="_compute_sale",
        store=True
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, compute="_compute_sale", store=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        default=lambda _: fields.Date.add(fields.Date.today(), months=3),
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, compute="_compute_sale", store=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("west", "West"),
            ("east", "East"),
        ],
        help="Defines the orientation of the garden area."
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive."
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive."
    )

    @api.depends("state", "offer_ids.status", "offer_ids.price", "offer_ids.partner_id")
    def _compute_sale(self):
        for record in self:
            if record.state in ["sold", "cancelled"]:
                continue
            accepted_offer = record.offer_ids.filtered(lambda o: o.status == "accepted")
            if accepted_offer:
                record.selling_price = accepted_offer.price
                record.buyer_id = accepted_offer.partner_id
                record.state = "accepted"
            else:
                record.selling_price = 0.0
                record.buyer_id = False
                record.state = "received" if record.offer_ids else "new"
        return True

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_minimum(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=2)
                and float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0
            ):
                raise ValidationError(self.env._("The selling price cannot be lower than 90%% of the expected price."))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def delete_property(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(self.env._("Only new and cancelled properties can be deleted."))

    def action_set_sold(self):
        self.ensure_one()
        for record in self:
            if record.state != "cancelled":
                record.state = "sold"
            else:
                raise UserError(self.env._("Cancelled properties cannot be sold."))
        return True

    def action_set_cancelled(self):
        self.ensure_one()
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            else:
                raise UserError(self.env._("Sold properties cannot be cancelled."))
        return True
