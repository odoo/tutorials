# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class Estate(models.Model):
    _name = "estate_property"
    _description = "RE Initial Model"
    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    postcode = fields.Text()
    date_availability = fields.Date(
        copy=False, default=fields.Date.today() + relativedelta(months=+3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )

    state = fields.Selection(
        string="State",
        required=True,
        readonly=True,
        default="new",
        copy=False,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Canceled"),
        ],
    )
    property_type_id = fields.Many2one("property_type")
    buyer = fields.Many2one("res.partner", copy=False)
    salesperson = fields.Many2one("res.users", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("property_tag")
    property_offer_ids = fields.One2many("property_offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("property_offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.mapped("property_offer_ids.price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0  # Or None if you prefer
            self.garden_orientation = False  # Or None if you prefer

    def action_sell_property(self):
        for record in self:
            record.state = "sold"

    def action_cancel_property(self):
        for record in self:
            record.state = "cancelled"
