from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyModel(models.Model):
    _name = "estate.property"
    _description = "The estate property model"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Date.add(fields.Date.today(), months=3)
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
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="new",
        required=True,
        copy=False,
    )

    property_type_id = fields.Many2one(
        "estate.property.types", string="Property Type", copy=False
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tags", "partner_id", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer("Total Area", compute="_compute_total_area")
    best_offer = fields.Float("Best Price", compute="_compute_best_offer")
    company_id= fields.Many2one("res.company", default=lambda self:self.env.company)

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price>0)",
            "The expected price must be strictly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price>0)",
            "The selling must be positive",
        ),
    ]

    @api.constrains("selling_price")
    def check_selling_price(self):
        for record in self:
            if (
                float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_rounding=2,
                )
                < 0
            ):
                raise ValidationError(
                    "the selling price cannot be lower than 90% of the expected price"
                )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.ondelete(at_uninstall=False)
    def _unlink_except_state_new_or_cancelled(self):
        for record in self:
            if record.state != "new" or record.state != "cancelled":
                raise UserError("only new and cancelled property can deleted")

    def action_set_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("cancelled property can not be sold")
            else:
                record.state = "sold"
        return True

    def action_set_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("sold property can not be cancelled")
            else:
                record.state = "cancelled"
        return True
