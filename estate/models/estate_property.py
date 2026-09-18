from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _check_positive_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be stricly positive",
    )
    _check_positive_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive",
    )

    name = fields.Char(required=True)
    postcode = fields.Char()
    description = fields.Text()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    best_price = fields.Float(compute="_find_best_price")
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden area (sqm)")
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="The garden orientation",
    )
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        copy=False,
        required=True,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tags_ids = fields.Many2many("estate.property.tag")
    buyer = fields.Many2one("res.partner", copy=False)
    salesman = fields.Many2one("res.users", default=lambda self: self.env.user)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.depends("living_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _find_best_price(self):
        for record in self:
            if not record.offer_ids:
                record.best_price = 0
            else:
                record.best_price = max(record.offer_ids.mapped("price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_sold_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("Cancelled property cannot be sold."))
            record.state = "sold"
        return True

    def action_cancel_property(self):
        for record in self:
            record.state = "cancelled"
        return True
