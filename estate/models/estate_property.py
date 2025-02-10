from odoo import fields, models, api
from datetime import date, timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate App"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: date.today() + timedelta(days=90)
    )
    expected_price = fields.Float()
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    is_garage = fields.Boolean(string="Garage")
    is_garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_reject", "Offer Rejected"),
            ("offer_accept", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type")
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        ondelete="restrict",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        ondelete="restrict",
        copy=False,
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if not record.offer_ids:
                record.best_offer = 0
                continue
            record.best_offer = max(record.offer_ids.mapped("price"))

    @api.onchange("is_garden")
    def _onchange_is_garden(self):
        if self.is_garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False
