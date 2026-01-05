from odoo import fields, models, api


class homePlan(models.Model):
    _name = "home.plan"
    _description = "this is home plan"

    name = fields.Char("Plan Name", required=True, default="Unknown")
    description = fields.Char("Description")
    postcode = fields.Char("Post code", required=True)
    date_availability = fields.Datetime(
        "Available till",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    expected_price = fields.Float("Expected Price")
    selling_price = fields.Float("Selling price", copy=False, readonly=True)
    bedrooms = fields.Integer("bedrooms", default="2")
    living_area = fields.Integer("Living area")
    facades = fields.Integer("facades")
    Garage = fields.Boolean("Garage", default=True)
    Garden = fields.Boolean("Garden")
    Garden_area = fields.Integer("Garden area")
    total_area = fields.Float("total area", compute="_compute_balance", store=True)
    best_price = fields.Float("best price", compute="_compute_offer")
    active = fields.Boolean("Active", default=True)
    property_type_id = fields.Many2one("estate.property.type")
    Salesman = fields.Many2one("res.users", default=lambda self: self.env.user)
    Buyer = fields.Many2one("res.partner", copy=False)
    property_tag_id = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    State = fields.Selection(
        [
            ("New", "new"),
            ("Offer Received", "offer received"),
            ("Offer Accepted", "offer accepted"),
            ("Sold", "sold"),
            ("Cancelled", "cancelled"),
        ],
        default="New",
        copy=False,
    )

    Garden_orientation_direction = fields.Selection(
        [("North", "north"), ("East", "east"), ("West", "west"), ("South", "south")]
    )

    @api.depends("living_area", "Garden_area")
    def _compute_balance(self):
        for line in self:
            line.total_area = line.living_area + line.Garden_area

    @api.depends("offer_ids")
    def _compute_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)
