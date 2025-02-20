from odoo import api,  fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property"
    _order = "id desc"
    _inherit = "mail.thread"

    name = fields.Char(
        "Property Name", required=True, tracking=True
    )  # required make property not nullable
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )  # lambda function delays the execution of this until the record is created
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default="2")
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientations",
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("west", "West"),
            ("south", "South"),
        ],
        help="this is used to select orientations of garden",
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        tracking=True,
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", copy=False
    )  # a buyer is a external person - therefore in partner relation
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user, domain=lambda self:[('company_id' ,'=', self.env.company.id)]
    )  # a salesman is considered a internal entity - therefore in user relation
    tag_ids = fields.Many2many("estate.property.tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(
        "Total Area (sqm)",
        compute="_compute_total_area",
        help="Calculate by adding Living area and Garden Area",
    )
    best_price = fields.Float("Best Price", compute="_compute_best_price")
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    property_image = fields.Image()

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = (
                max(record.offer_ids.mapped("price")) if record.offer_ids else 0
            )  # sets best price only when record of offers are added

    @api.onchange("garden")
    def _onchange_(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False
            # onchange can also be used to return warning

    # sql constraint to check if expected price, selling price are positive
    _sql_constraints = [
        (
            "check_positive_expected_price",
            "CHECK(expected_price > 0)",
            "The Expected Price of the Property must be a positive value",
        ),
        (
            "check_positive_selling_price",
            "CHECK(selling_price >= 0)",
            "The Selling Price of the Property must be a positive value",
        ),
    ]

    # python constraint for selling price not lower than 90% of expected price
    @api.constrains("selling_price")
    def _check_selling_price_minimum_value(self):
        for record in self:
            # selling price is zero by deafult, this checks that it do enter with default value
            if not float_is_zero(record.selling_price, precision_digits=1):
                minimum_price = record.expected_price * 0.9
                if (
                    float_compare(
                        record.selling_price, minimum_price, precision_digits=2
                    )
                    == -1
                ):
                    raise ValidationError(
                        "The Selling Price cannot be lower than 90% of Expected Price"
                    )
    @api.model_create_multi
    def create(self, vals_list):
        created_property = super().create(vals_list)
        # breakpoint()
        # print(created_property)
        for record in created_property:
            message = "{} created a property named ' {} '".format(self.env.user.name, record.name)
            record.message_post(body=message)
        return created_property

    @api.ondelete(at_uninstall=False)
    def _unlink_expect_state_new_or_Cancelled(self):
        if any(record.state not in ("new", "cancelled") for record in self):
            raise ValidationError("Only New or Cancelled property can be deleted")

    # functions to set status of property to sold or cancelled
    def action_set_property_status_sold(self):
        for record in self:
            if record.state == "cancelled":
                message = "Cancelled Property cannot be Sold"
                raise UserError(message)
            elif not record.buyer_id:
                message = "Buyer must be assigned to sell Property"
                raise UserError(message)
            else:
                record.state = "sold"
                record.message_post(body="Property Sold to buyer : {}".format(record.buyer_id.name))
            return True

    def action_set_property_status_cancel(self):
        for record in self:
            if record.state == "sold":
                message = "Sold Property cannot be Cancelled"
                raise UserError(message)
            else:
                record.state = "cancelled"
            return True 
