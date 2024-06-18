from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    _order = "id desc"
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", _("A property expected price must be strictly positive")),
        ("check_selling_price", "CHECK(selling_price >= 0)", _("The selling price must be positive")),
    ]

    name = fields.Char("Title", required=True, readonly=False, copy=False, default="New")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        required=True,
        copy=False,
        string="Status",
    )

    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From", copy=False, default=fields.Datetime.add(fields.Datetime.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float("Total Area (sqm)", compute="_compute_area")
    best_price = fields.Float("Best Offer", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_area(self) -> None:
        for estate_property in self:
            estate_property.total_area = estate_property.living_area + estate_property.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self) -> None:
        for estate_property in self:
            estate_property.best_price = (
                max(estate_property.offer_ids.mapped("price")) if estate_property.offer_ids else 0
            )

    @api.constrains("selling_price")
    def _check_selling_price(self) -> None:
        filtered_property = self.filtered("selling_price")
        if any(tools.float_compare(p.selling_price, p.expected_price * 0.9, 0) == -1 for p in filtered_property):
            raise ValidationError(_("Selling price to low (< 90% of expected price)"))

    @api.onchange("garden")
    def _onchange_garden(self) -> None:
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def ondelete(self) -> None:
        if any(p.state not in ("new", "canceled") for p in self):
            raise UserError(_("Property status must be new or canceled"))

    @api.model
    def create(self, val):
        if val.get("name", _("New")) == _("New"):
            val["name"] = self.env["ir.sequence"].next_by_code("estate.property") or _("New")
        return super().create(val)

    def action_sold(self) -> bool:
        self.ensure_one()
        if self.state == "canceled":
            raise UserError(_("An property canceled can't be sold"))
        self.state = "sold"
        return True

    def action_cancel(self) -> bool:
        self.ensure_one()
        if self.state == "sold":
            raise UserError(_("An property sold can't be canceled"))
        self.state = "canceled"
        return True
