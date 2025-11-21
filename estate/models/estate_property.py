from odoo import fields, models, api, exceptions
from odoo.tools import float_compare


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property Info"

    name = fields.Char(required=True, translate=True, string="Title")
    description = fields.Text(translate=True)
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Datetime.add(fields.Datetime.today(), months=3),
        string="Available From",
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("west", "West"),
            ("south", "South"),
        ],
    )
    active = fields.Boolean(default=True)
    status = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[
            ("new", "New"),
            ("offer_recieved", "Offer Recieved"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy="False")
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )

    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(
        compute="_compute_total_area",
        string="Total Area(sqm)",
    )
    best_offer = fields.Float(
        compute="_compute_best_price",
        string="Best Offer",
    )

    _check_positive_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Prices Must Be Positive",
    )

    _check_positive_selling_price = models.Constraint(
        "CHECK(selling_price > 0)",
        "Prices Must Be Positive",
    )

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else None

    def button_sell_property(self):
        for record in self:
            if record.status == "cancelled":
                raise exceptions.UserError("Property Cancelled")
            record.status = "sold"
        return True

    def cancel_property_action(self):
        for record in self:
            if record.status == "sold":
                raise exceptions.UserError("Property Sold")
            record.status = "cancelled"
        return True

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, record.expected_price * 0.90, 2) < 0:
                raise exceptions.ValidationError("The selling price is too low")
