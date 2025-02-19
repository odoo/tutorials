from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyModel(models.Model):
    _name = "estate.property"
    _description = "Defines the model of a real estate property"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Date of availability",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string="Number of bedrooms", default=2)
    living_area = fields.Integer()
    facades = fields.Integer(string="Number of facades")
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
        string="Garden orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    sales_person_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(string="Total area", compute="_compute_total_area")
    best_offer = fields.Float(string="Best offer", compute="_compute_best_offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for estate_property in self:
            estate_property.total_area = estate_property.living_area + estate_property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for estate_property in self:
            estate_property.best_offer = max(estate_property.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sell_property(self):
        if any(estate_property.state == "cancelled" for estate_property in self):
            raise UserError("Cannot sell a cancelled property")
        self.state = "sold"
        return True

    def action_cancel_property(self):
        if any(estate_property.state == "sold" for estate_property in self):
            raise UserError("Cannot cancel a sold property")
        self.state = "cancelled"
        return True
