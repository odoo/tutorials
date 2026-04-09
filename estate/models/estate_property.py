from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="Property State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    sales_man = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag = fields.Many2many("estate.property.tag", string="Tags")
    offer = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for records in self:
            records.total_area = records.living_area + records.garden_area

    @api.depends("offer.price")
    def _compute_best_price(self):
        for records in self:
            prices = records.mapped("offer.price")
            records.best_price = max(prices) if prices else 0

    @api.onchange("garden")
    def _on_change_garden(self):
        for records in self:
            if records.garden:
                records.garden_area = 10
                records.garden_orientation = "north"
            else:
                records.garden_area = False
                records.garden_orientation = False
