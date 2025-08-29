from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Real Estate Advertisement Model"
    _order = "id desc"

    active = fields.Boolean(default=True)
    bedrooms = fields.Integer(default=2)
    best_price = fields.Float(compute="_compute_best_price", store=True, default=0.0)
    buyer = fields.Many2one("res.partner", readonly=True)
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.today() + timedelta(days=90),
    )
    description = fields.Text()
    expected_price = fields.Float(required=True)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Select the direction the garden faces",
    )
    living_area = fields.Integer()
    name = fields.Char(required=True)
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id")
    postcode = fields.Char()
    property_type_id = fields.Many2one("estate.property.type")
    salesman = fields.Many2one("res.users")
    selling_price = fields.Float(readonly=True, copy=False)
    state = fields.Selection(
        string="State",
        default="new",
        required=True,
        copy=False,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    tag_ids = fields.Many2many("estate.property.tag")
    total_area = fields.Float(compute="_compute_total_area", store=True)

    _sql_constraints = [
        (
            "check_property_expected_price",
            "CHECK(expected_price > 0)",
            "Property Expected Price must be a valid value",
        ),
        (
            "check_property_selling_price",
            "CHECK(selling_price >= 0)",
            "Property Selling Price must be positive",
        ),
    ]

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_percentage(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            if (
                float_compare(
                    record.selling_price,
                    (record.expected_price * 0.9),
                    precision_rounding=0.01,
                )
                < 0
            ):
                raise ValidationError(
                    "Selling Price of the property can not be less than 90 percent of the expected Price"
                )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            self.write(
                {
                    "best_price": max(record.offer_ids.mapped("price"), default=0.0),
                }
            )
        if record.best_price > 0.0:
            record.state = "offer_received"

    @api.onchange("garden")
    def _set_garden_default_values(self):
        if self.garden:
            self.write({"garden_area": 10, "garden_orientation": "north"})
        else:
            self.write({"garden_area": 0, "garden_orientation": ""})

    def action_property_sold(self):
        if float_is_zero(self.selling_price, precision_rounding=0.01):
            raise UserError(
                "Atleast one offer must be accepted before selling the property"
            )
        self.state = "sold"

    def action_property_cancelled(self):
        self.state = "cancelled"
        for offer in self.offer_ids:
            if not offer.status:
                offer.status = "refused"

    @api.ondelete(at_uninstall=False)
    def _check_before_deleting_record(self):
        # more than one record can be present in recordset
        for record in self:
            if record.state in ["offer_received", "offer_accepted", "sold"]:
                raise UserError(
                    "Properties with received offers, accepted offers, or that have been sold cannot be deleted."
                )
