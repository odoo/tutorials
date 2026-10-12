from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is a dummy table"

    def _cal_date(self):
        return fields.Date.today() + relativedelta(months=3)

    name = fields.Char(translate=True, required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=_cal_date
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True, copy=False)
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
        default="north"
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        compute="_compute_state",
        store=True
    )
    active = fields.Boolean("Active", default=True)
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many(
        "estate.property.tag",
        relation="losbo_property_propertyTag",
        column1="estate_property_id",
        column2="estate_property_tag_id"
    )
    buyer = fields.Many2one("res.partner", string="buyer", copy=False)
    user_id = fields.Many2one(
        "res.users", string="salesperson", default=lambda self: self.env.user
    )
    offer_ids = fields.One2many("estate.property.offers", "property_id")
    total_offers = fields.Integer(compute="_compute_offers")
    total_area = fields.Float(compute="_compute_area")
    best_price = fields.Integer(compute="_compute_price")

    _check_expected_price = models.Constraint(
        'check(expected_price>0)',
        'Expected price must be strictly positive'
    )

    _check_selling_price = models.Constraint(
        'check(selling_price>=0)',
        'Selling price must be positive'
    )

    def copy_data(self, default=None):
        default = dict(default or {})
        vals_list = super().copy_data(default=default)
        if "name" not in default:
            for template, vals in zip(self, vals_list):
                vals["name"] = _("%s (copy)", template.name)
        return vals_list

    @api.constrains('selling_price', 'expected_price')
    def _selling_price_check(self):
        for rec in self:
            if rec.selling_price < (rec.expected_price * 0.9):
                raise ValidationError(
                    "Selling Price Cannot be lower than %s%% of the expected price." % 90
                )

    @api.depends("offer_ids")
    def _compute_offers(self):
        for record in self:
            record.total_offers = len(record.offer_ids)

    @api.constrains("name", "description")
    def _check_description(self):
        for record in self:
            if record.name == record.description:
                raise ValidationError(
                    "Fields name and description should not be equal")

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_price(self):
        for records in self:
            records.best_price = max(
                records.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for records in self:
            if records.garden:
                records.garden_area = 10
                records.garden_orientation = "north"
            else:
                records.garden_area = 0
                records.garden_orientation = ""

    @api.depends("offer_ids", "offer_ids.status")
    def _compute_state(self):
        for record in self:
            if len(record.offer_ids) == 0:
                record.state = "new"
            elif record.state not in ("sold", "cancelled"):
                if "accepted" in record.offer_ids.mapped("status"):
                    record.state = "offer_accepted"
                else:
                    record.state = "offer_received"

    def property_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled property cannot be sold")
            elif record.state == "sold":
                raise UserError("Property is already sold")
            if "accepted" in record.offer_ids.mapped("status"):
                record.state = "sold"
            else:
                raise UserError("There should be one accepted offer")

    def property_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be cancelled")
            elif record.state == "cancelled":
                raise UserError("Property is already cancelled")
            record.state = "cancelled"
