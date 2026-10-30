from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is a dummy table"
    _order = "id desc"

    def _cal_date(self):
        return fields.Date.today() + relativedelta(months=3)

    name = fields.Char(translate=True, required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=_cal_date)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Direction",
        default="north",
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    active = fields.Boolean("Active", default=True)
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Types")
    property_tag_ids = fields.Many2many(
        "estate.property.tag",
        relation="losbo_property_propertyTag",
        column1="estate_property_id",
        column2="estate_property_tag_id",
    )
    buyer = fields.Many2one("res.partner", string="buyer", copy=False)
    user_id = fields.Many2one(
        "res.users", string="salesperson", default=lambda self: self.env.user
    )
    offer_ids = fields.One2many("estate.property.offers", "property_id")
    total_offers = fields.Integer(compute="_compute_total_offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Integer(compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "check(expected_price>0)", "Expected price must be strictly positive"
    )

    _check_selling_price = models.Constraint(
        "check(selling_price>=0)", "Selling price must be positive"
    )

    @api.constrains("selling_price")
    def _selling_price_check(self):
        for rec in self:
            if rec.selling_price < (rec.expected_price * 0.9):
                raise ValidationError(
                    "Selling Price Cannot be lower than 90% of the expected price."
                )

    @api.constrains("name", "description")
    def _check_description(self):
        for record in self:
            if record.name == record.description:
                raise ValidationError(
                    "Fields name and description should not be equal")

    @api.depends("offer_ids")
    def _compute_total_offers(self):
        for record in self:
            record.total_offers = len(record.offer_ids)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for records in self:
            records.best_price = max(
                records.offer_ids.filtered(lambda r: r.status != "refused").mapped(
                    "price"
                ),
                default=0,
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        for records in self:
            if records.garden:
                records.garden_area = 10
                records.garden_orientation = "north"
            else:
                records.garden_area = 0
                records.garden_orientation = ""

    @api.ondelete(at_uninstall=False)
    def _unlink_new_cancel_state(self):
        for rec in self:
            if rec.state not in ("new", "cancelled"):
                raise UserError(
                    "New or Cancelled Properties cannot be deleted")

    def action_property_sold(self):
        self.ensure_one()

        if self.state == "cancelled":
            raise UserError("Cancelled property cannot be sold")
        elif self.state == "sold":
            raise UserError("Property is already sold")
        if self.state == "offer_accepted":
            self.state = "sold"
        else:
            raise UserError("There should be one accepted offer")

    def action_property_cancel(self):
        self.ensure_one()

        if self.state == "sold":
            raise UserError("Sold property cannot be cancelled")
        elif self.state == "cancelled":
            raise UserError("Property is already cancelled")
        self.state = "cancelled"

    def copy_data(self, default=None):
        default = dict(default or {})
        vals_list = super().copy_data(default=default)
        if "name" not in default:
            for template, vals in zip(self, vals_list):
                vals["name"] = _("%s (copy)", template.name)
        return vals_list
