from odoo import api, fields, models
from odoo.exceptions import UserError

DEFAULT_GARDEN_AREA = 10
DEFAULT_GARDEN_ORIENTATION = "north"


class PropertyModel(models.Model):
    _name = "estate.property"
    _description = "Estate Property model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
    best_offer = fields.Float(compute="_get_highest_price")
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    total_living_area = fields.Integer(compute="_compute_total_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        required=True,
        copy=False,
        default="new"
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_living_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _get_highest_price(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price")) if record.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = DEFAULT_GARDEN_AREA
                record.garden_orientation = DEFAULT_GARDEN_ORIENTATION
            else:
                record.garden_area = 0
                record.garden_orientation = None

    def mark_as_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be set as sold.")
            record.state = "sold"
        return True

    def mark_as_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be set as cancelled.")
            record.state = "cancelled"
        return True
