from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    _order = "id desc"

    name = fields.Char(required=True, string="Title")
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    available_from = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(
        string="Selling Price", default=0, copy=False, readonly=True
    )
    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)", default=0)
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)", default=0)
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        default=False,
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )

    # Defining Many2One relationship
    property_type_id = fields.Many2one("property.type", string="Property Type")
    # means multiple records can have a single property_type

    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tags_ids = fields.Many2many("property.tags", string="Tags")
    offer_ids = fields.One2many("property.offers", "property_id", string="Offers")

    total_area = fields.Integer(string="Total Area", compute="_compute_total")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")

    # Compute total_area
    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # Compute best_price from all the offers
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    # checking garden automatically set garden_area and garden_orienatation
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = False
            self.garden_orientation = False

    # mark property as sold when sold button is clicked
    def sold_action(self):
        if self.state == "cancelled":
            raise UserError("Cancelled properties can't be sold!")
        else:
            self.state = "sold"
        return True

    # mark property as cancelled when cancel button is clicked
    def cancel_action(self):
        if self.state == "sold":
            raise UserError("Sold properties can't be cancelled!")
        else:
            self.state = "cancelled"
        return True

    # sql constraints
    # expected price must not be negative
    _sql_constraints = [
        (
            "expected_price",
            "CHECK(expected_price >0)",
            "A expected price must be strictly positive",
        ),
        (
            "selling_price",
            "CHECK(selling_price >= 0)",
            "A selling price must be positive",
        ),
    ]

    # python constraints to check whether selling price is below 90% of expected price
    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            is_offer_accepted = any(
                offer.status == "accepted" for offer in record.offer_ids
            )
            # check if selling price is greater than zero (i.e selling price is not zero)
            # skip the validation if no offers yet created.
            # A > B, it returns 1
            # A == B, it returns 0
            # A < B, it returns -1
            if is_offer_accepted and not float_is_zero(
                record.selling_price,
                precision_digits=2,
            ):
                if (
                    float_compare(
                        record.selling_price,
                        0.9 * record.expected_price,
                        precision_digits=2,
                    )
                    == -1
                ):
                    raise ValidationError(
                        "The selling price must be at least 90% of expected price! You must reduce the expected price in order to accept the offer."
                    )
