from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available from",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        required=True,
    )
    expected_price = fields.Float(
        required=True,
        string="Expected Price",
        help="The expected price of the property",
    )
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2, required=True)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Orientation of the garden",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Integer(compute="_compute_best_price")

    _check_positive_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "The selling price can't be negative."
    )
    _check_positive_expected_price = models.Constraint(
        "CHECK(expected_price >= 0)", "The expected price can't be negative."
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids", "offer_ids.state")
    def _compute_best_price(self):
        for record in self:
            offers = self.offer_ids.filtered(lambda offer: offer.state != "refused")
            record.best_price = max(offers.mapped("price")) if offers else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10
        self.garden_orientation = "north"  # return {'warning': {  #     'title': ("Warning"),  #     'message': ('Garden area and description set')}}

    def action_do_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(self.env._("Sold properties cannot be cancelled"))
            else:
                record.state = "cancelled"
        return True

    def action_do_sell(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(self.env._("Cancelled properties cannot be sold"))
            else:
                accepted_offer = self.env["estate.property.offer"].search([
                    ("property_id", "=", record.id),
                    ("state", "=", "accepted"),
                ])
                if not accepted_offer:
                    raise UserError(self.env._("No accepted offer found"))
                record.selling_price = accepted_offer.price
                record.buyer_id = accepted_offer.partner_id.id
                record.state = "sold"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price != 0 and (
                float_compare(
                    record.selling_price,
                    0.9 * record.expected_price,
                    precision_digits=2,
                )
                == -1
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price"
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_prevent_if_not_new_or_sold(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError(
                    self.env._("Only new or cancelled properties can be deleted.")
                )
