from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Table for property test tutoriel"

    name = fields.Char("Title", required=True, default="Unknown")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    property_type_id = fields.Many2one("estate.property.type")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    tags_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    total_area = fields.Integer(compute="_total_area", readonly=True)
    best_price = fields.Float(compute="_best_price", readonly=True, string="Best Offer")

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
            return
        self.garden_orientation = self.garden_area = None

    @api.depends("offer_ids.price")
    def _best_price(self):
        for record in self:
            if len(best := self.mapped("offer_ids.price")) < 1:
                record.best_price = 0
                continue
            record.best_price = max(best)

    @api.depends("living_area", "garden_area")
    def _total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
