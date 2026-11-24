from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    age = fields.Interger()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False,
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
        ]
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="new",
        copy=False,
    )
    
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type"
    )

    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags"
    )
    
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
    )

    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )
    
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )
    
    total_area = fields.Integer(
        compute="_compute_total_area"
    )
    
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (
                record.living_area + record.garden_area
            )
            
    best_price = fields.Float(
        compute="_compute_best_price"
    )
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(
                record.offer_ids.mapped("price"),
                default=0.0
            )
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False
            
    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(
                    "A canceled property cannot be sold."
                )
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(
                    "A sold property cannot be canceled."
                )
            record.state = "cancelled"
        return True
    
    _sql_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Expected price must be strictly positive.",
    )

    _sql_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "Selling price cannot be negative.",
    )
    
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):

                if float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=2
                ) < 0:
                    raise ValidationError(
                        "Selling price cannot be less than "
                        "90% of the expected price."
                    )
                    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_new_or_canceled(self):
        if any(
            record.state not in ("new", "canceled")
            for record in self
        ):
            raise UserError(
                "You cannot delete a property "
                "that is not new or canceled."
            )
    