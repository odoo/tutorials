from odoo import api, fields, models
from datetime import timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Model containing basic info of a property"

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text("Notes")
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Date.today() + timedelta(days=90), copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean("Active", default=True)
    total_area = fields.Integer(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best_offer")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    tag_ids = fields.Many2many("estate.property.tag")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("west", "West"),
            ("south", "South"),
        ]
    )
    state = fields.Selection(
        string="State",
        required=True,
        copy=False,
        default="new",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)
