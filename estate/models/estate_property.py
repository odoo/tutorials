from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Model"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    postcode = fields.Text(string="Postcode")
    date_availability = fields.Date(string="Date Availability")
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Integer(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )

    active = fields.Boolean(default=False, string="Active")

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received "),
            ("offer_accepted", "Offer Accepted"),
            ("Cancelled", "Cancelled"),
        ],
        string="State",
        default="new",
        copy=False,
    )

    # property will have Many to one relation with property since many properties can belong to one property

    property_type_id = fields.Many2one("estate.property.type", "Property Type")

    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        copy=False,
        default=lambda self: self.env.user,
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer(
        compute="_compute_total_property_area", string="Total Area"
    )

    best_price = fields.Integer(compute="_compute_best_price", string="Best Price")

    status = fields.Char(default="new", string="Status")

    @api.depends("garden_area", "living_area")
    def _compute_total_property_area(self):
        for area in self:
            self.total_area = self.garden_area + self.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            offers_list = record.mapped("offer_ids.price")
            if offers_list:
                record.best_price = max(offers_list)
            else:
                record.best_price = 0

    # on change of garden status , update gardern area and its orientation

    @api.onchange("garden")
    def _onchange_garden_status(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
            return
        self.garden_area = 0
        self.garden_orientation = ""

    # acts when property is sold
    # In case property is cancelled it cannot be sold
    def action_sell_property(self):
        # dictionary for the property status
        property_sell_status_dict = {"new": True, "sold": True, "cancelled": False}

        for record in self:
            print("the object on sell action", record.read())
            if property_sell_status_dict[record.status]:
                record.status = "sold"
            else:
                raise UserError("Cancelled property cannot be sold.")

    # action in case of cancel property button
    #  If property is sold than Cannot be cancelled

    def action_cancel_property_selling(self):
        property_cancel_status_dict = {
            "new": True,
            "cancelled": True,
            "sold": False,
        }
        for record in self:
            if property_cancel_status_dict[record.status]:
                record.status = "cancelled"
            else:
                raise UserError("Sold  property cannot be cancelled.")
