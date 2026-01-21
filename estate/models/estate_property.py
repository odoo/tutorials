from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Name", required=True)
    postcode = fields.Char(string="Postcode")
    available_from = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )

    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True)

    description = fields.Text(string="Description")
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        readonly=True,
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="State",
        default="new",
        required=True,
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        index=True,
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = ""
        else:
            self.garden_area = 10
            self.garden_orientation = "north"

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                message = "Sold properties cannot be canceled"
                raise UserError(message)
            record.state = "canceled"

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                message = "Canceled properties cannot be sold"
                raise UserError(message)
            record.state = "sold"
