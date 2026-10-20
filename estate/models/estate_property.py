from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    name = fields.Char(required=True, translate=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Datetime.today() + relativedelta(months=3),
    )

    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden area (sqm)")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("west", "West"), ("east", "East")]
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer(compute="_compute_total_area")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price") + [0])

    @api.onchange("garden")
    def _ongarden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None
