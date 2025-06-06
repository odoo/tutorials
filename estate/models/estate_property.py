from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateUser(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
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
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
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
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", string="Property Type"
    )
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tags_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
    )
    total_area = fields.Integer(
        compute="_compute_total_area",
        store=True,
    )
    best_offer = fields.Float(
        compute="_compute_best_offer",
        store=True,
    )

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be greater than 0.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price must be greater than or equal to 0.",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + (record.garden_area or 0)

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            best_price = max(record.offer_ids.mapped("price") or [0.0])
            record.best_offer = best_price

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"

    @api.onchange("offer_ids")
    def _onchange_offer_ids(self):
        if self.offer_ids and not self.selling_price:
            self.state = "offer_received"

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cannot sell a cancelled property.")
            else:
                record.state = "sold"
                return True
        return False

    def action_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Cannot cancel a sold property.")
            else:
                record.state = "cancelled"
                return True
        return False
