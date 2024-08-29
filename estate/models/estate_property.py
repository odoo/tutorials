from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Table contains real estate properties."
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.today() + relativedelta(months=3),
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
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        copy=False,
        default="new",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        tracking=True,
    )
    salesman_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer")
    property_image = fields.Binary("Property Image")
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    _sql_constraints = [
        (
            "positive_expected_price",
            "CHECK(expected_price > 0.0)",
            "A property expected price must be strictly positive",
        ),
        (
            "positive_selling_price",
            "CHECK(selling_price >= 0.0)",
            "A property selling price must be positive",
        ),
    ]

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if (
                    float_compare(
                        record.selling_price,
                        0.9 * record.expected_price,
                        precision_digits=2,
                    )
                    == -1
                ):
                    raise ValidationError(
                        "Selling price cannot be lower than 90% of the expected price"
                    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("Sold property can not be canceled."))
            else:
                record.state = "canceled"
        return True

    def action_sold_property(self):
        for record in self:
            if record.state == "canceled":
                raise UserError(_("Canceled property can not be sold."))
            else:
                record.state = "sold"
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_except_certain_state(self):
        for record in self:
            if record.state not in ["new", "canceled"]:
                raise UserError(_("Only new or canceled property can be deleted."))
