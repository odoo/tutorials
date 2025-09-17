from odoo import fields, models, api, exceptions, tools
from datetime import timedelta


class estate_property(models.Model):
    _name = "estate.property"
    _description = "estate.property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        string="Available From",
        default=lambda self: fields.Date.today() + timedelta(days=90),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True, copy=False, compute="_set_selling_price"
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Float(compute="_compute_total_area")
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
        required=True,
        default="new",
        copy=False,
        selection=[
            ("new", "New"),
            ("offer Received", "Offer Received"),
            ("offer Accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    property_type_id = fields.Many2one("estate.property.type", string="Model")
    sales_user_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer_partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(compute="_get_highest_price")
    has_accepted_offer = fields.Boolean(default=False)

    # ---------------------------------------------------------------------------------------------------------
    #   Compute Functions

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _get_highest_price(self):
        for record in self:
            record.best_price = max(record.mapped("offer_ids.price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = ""

    @api.depends("offer_ids.status", "has_accepted_offer")
    def _set_selling_price(self):
        for record in self:
            if not len(record.offer_ids):
                record.selling_price = 0
            else:
                if "accepted" not in set(record.mapped("offer_ids.status")):
                    record.selling_price = 0
                    record.has_accepted_offer = False
                else:
                    id = record.mapped("offer_ids.status").index("accepted")
                    record.selling_price = record.mapped("offer_ids.price")[id]
                    record.has_accepted_offer = True

    # ---------------------------------------------------------------------------------------------------------
    #   Public Functions

    def set_state_cancelled(self):
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            else:
                raise exceptions.UserError(
                    (
                        "You can't change the offer's state to Cancelled after the offer has been sold"
                    )
                )

        return True

    def set_state_sold(self):
        for record in self:
            if record.state != "cancelled":
                record.state = "sold"
            else:
                raise exceptions.UserError(
                    (
                        "You can't change the offer's state to Sold after the offer has been cancelled"
                    )
                )
        return True

    # ---------------------------------------------------------------------------------------------------------
    #   Constraints

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price of a propriety needs to be strictly positive",
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price of a propriety needs to be positive",
    )

    @api.constrains(
        "expected_price",
    )
    def _check_selling_price(self):
        print("A")
        for record in self:
            if not record.has_accepted_offer:
                return True

            if (
                tools.float_compare(
                    (record.expected_price * 0.9), record.selling_price, 2
                )
                >= 0
            ):
                raise exceptions.ValidationError(
                    "The selling price cant be lower than 90 percent of the expected price"
                )
