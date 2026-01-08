from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Storing Properties of Real Estate"

    name = fields.Char(string="name", required=True)
    description = fields.Text(string="description")
    postcode = fields.Char("postcode")
    date_availability = fields.Date(
        string="date availability",
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False,
    )
    expected_price = fields.Float(string="expected price", required=True)
    selling_price = fields.Float(string="selling price", copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )

    property_type_id = fields.Many2one("estate_property_type")
    property_tag_ids = fields.Many2many("estate_property_tag")
    salesman_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    offer_property_ids = fields.One2many("estate_property_offer", "property_id")
    total_area = fields.Float("Total Area(sqm)", compute="_compute_total_area")
    best_price = fields.Float("Best Price", compute="_compute_best_price")

    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
    )

    _expected_price_positive_check = models.Constraint(
        "CHECK(expected_price>0)", "The expected price must be strictly positive"
    )
    _selling_price_positive_check = models.Constraint(
        "CHECK(selling_price>=0)", "The selling price must be positive"
    )

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        self.total_area = self.garden_area + self.living_area

    @api.depends("offer_property_ids")
    def _compute_best_price(self):
        self.best_price = max(self.offer_property_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_gaden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        if (           
            self.selling_price
            and (float_compare(self.selling_price, (0.9 * self.expected_price), 2))
            == -1
        ):
             
            raise ValidationError(
                "The selling price is must greater than 90% of expected price"
            )

    def action_set_sold(self):
        if self.state == "cancelled":
            raise UserError(message="The cancelled property cant be sold")
        self.state = "sold"
        return True

    def action_set_cancelled(self):
        if self.state == "sold":
            raise UserError(message="Sold property can not be cancelled")
        self.state = "cancelled"
        return True
