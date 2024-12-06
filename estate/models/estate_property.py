from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Table"
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        index=True,
        tracking=True,
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one("res.users", string="Buyer", copy=False)
    name = fields.Char("Name", required=True)
    description = fields.Text("Description", required=True)
    postcode = fields.Char("PostCode", required=True)
    date_availability = fields.Date("Availability Date", required=True, copy=False)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    expected_price = fields.Float("Expected Price", required=True)
    bedrooms = fields.Integer("Bedrooms", required=True, default=2)
    living_area = fields.Integer("Living Area", required=True)
    facades = fields.Integer("Facades", required=True)
    garage = fields.Boolean("Garage", required=True)
    garden = fields.Boolean("Garden", required=True)
    garden_area = fields.Integer("Garden Area", required=True)
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        "Garden Orientation",
        required=True,
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    active = fields.Boolean("Active", default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tags", string=" ")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string=" ")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
