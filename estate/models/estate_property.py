from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class Estate(models.Model):
    _name = "estate_property"
    _description = "real estate management"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_available = fields.Date(
        copy=False,
        default=lambda self: fields.Datetime.add(fields.Date.today(), months=3),
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
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one(comodel_name="estate.property_type")
    buyer_id = fields.Many2one(comodel_name="res.partner", copy=False)
    salesman_id = fields.Many2one(
        comodel_name="res.users", default=lambda self: self.env.user
    )
    property_tag_ids = fields.Many2many(
        comodel_name="estate.property_tag", string="Property Tags"
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property_offer",
        inverse_name="property_id",
        string="Offers",
    )
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "A property selling price must be positive"
    )
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property expected price must be strictly positive",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if (
                record.selling_price
                and float_compare(
                    record.expected_price * 0.9,
                    record.selling_price,
                    precision_rounding=0.01,
                )
                == 1
            ):
                raise ValidationError(
                    _("selling price must be least 90 percent of expected price")
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = False

    @api.ondelete(at_uninstall=False)
    def _unlink_except_state_is_cancelled_or_new(self):
        for record in self:
            if record.state not in ["cancelled", "new"]:
                raise UserError(
                    _("properties with state cancelled or new can only be deleted")
                )

    def action_mark_property_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("cancelled property can't be sold"))
            if record.selling_price:
                record._check_selling_price()
            else:
                raise ValidationError(
                    _("property cant be sold selling price must be greater than zero")
                )
            record.state = "sold"
        return True

    def action_mark_property_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("sold property can't be canceled"))
            record.state = "cancelled"
        return True
