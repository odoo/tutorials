from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Has Garage")
    garden = fields.Boolean("Has Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[("new", "New"), ("received", "Offer Received"), ("accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        required=True,
        copy=False,
        default="new",
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id", string="Test")
    total_area = fields.Integer(string="Total Area (sqm)", copy=False, readonly=True, compute="_compute_total_area")
    best_price = fields.Float(string="Best Price", copy=False, readonly=True, compute="_compute_best_price")

    @api.depends("living_area", "garden", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + (property.garden_area if property.garden else 0)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price")) if property.offer_ids else None

    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            has_garden = property.garden
            property.garden_area = 10 if has_garden else None
            property.garden_orientation = "north" if has_garden else None
