from odoo import api, fields, models


class Realestate(models.Model):
    _name = "realestate"
    _description = "Estate"
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
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
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    owner_id = fields.Many2one("owner")
    type_id = fields.Many2one("types")
    tag_ids = fields.Many2many("tags", string="Tags")
    seller_id = fields.Many2one("seller")
    buyer_id = fields.Many2one("buyer")
    offer_ids = fields.One2many("offer", "property_id")
    status = fields.Selection(related="offer_ids.status")
    price = fields.Float(related="offer_ids.price")
    validity = fields.Integer(related="offer_ids.validity")
    deadline = fields.Date(related="offer_ids.deadline")

    total_area = fields.Integer(compute="_compute_total")
    best_price = fields.Float(compute="_max_offer_price")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _max_offer_price(self):
        self.best_price = max(self.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""
