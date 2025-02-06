from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is a test description"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True, allow_negative=False)
    selling_price = fields.Integer(readonly=True, copy=False, allow_negative=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="state",
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
    property_type_id = fields.Many2one("estate.property.type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller = fields.Many2one(
        "res.partner", string="Seller", default=lambda self: self.env.company.id
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_area")
    best_price = fields.Float(compute="_compute_best_offer", default=0)
    cancelation = fields.Boolean(store=True, default=False)
    solded = fields.Boolean(store=True, default=False)
    _sql_constraints = [
        (
            "name_uniq",
            "unique(name, property_type_id.name, tags_ids.name)",
            "A tag with the same name and applicability already exists",
        )
    ]

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for area in self:
            if area:
                area.total_area = area.garden_area + area.living_area
            else:
                area.total_area = 0

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for offer in self:
            if offer.offer_ids:
                offer.best_price = max(offer.offer_ids.mapped("price"))
            else:
                offer.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def sold(self):
        if not self.cancelation:
            self.solded = True
            self.state = "sold"
        else:
            raise UserError("Cancelled Property cannot be sold!")

    def cancel(self):
        if not self.solded:
            self.cancelation = True
            self.state = "cancelled"
        else:
            raise UserError("Sold Property cannot be cancelled!")

    @api.constrains("expected_price")
    def _check_price_positive(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError("Expected Price cannot be negative!")
