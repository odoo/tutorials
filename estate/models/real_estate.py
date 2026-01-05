from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class RealEstate(models.Model):
    _name = "real_estate"
    _description = "Real Estate"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West"),
    ])
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="new",
    )
    active = fields.Boolean(default=False)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    sales_id = fields.Many2one("res.users", string="Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_totalarea")
    best_price = fields.Integer(compute="_compute_bestoffer")
    @api.depends("living_area", "garden_area")
    def _compute_totalarea(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_bestoffer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price") or [0] )

    @api.onchange("garden")
    def _garden_changes(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None
