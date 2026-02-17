from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property definition"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description", required=True)
    postcode = fields.Char(string="Postcode")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date()
    date_availability = fields.Date(
        string="Available From",
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Recieved"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="new",
        copy=False,
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one(
        "res.users",
        string=" Salesman",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one("res.partner", string=" Buyer")
    property_tag_ids = fields.Many2many("estate.property.tag")
    property_offer_ids = fields.One2many("estate.property.offer", "salesman_id")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area")
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        store=True,
    )

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):

        for estate in self:
            estate.total_area = estate.garden_area + estate.living_area

    @api.depends("property_offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.property_offer_ids:
                record.best_price = max(record.property_offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""
