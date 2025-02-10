from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Propery Model"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        default=(fields.Date.add(fields.Date.today(), months=3)),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    is_garage = fields.Boolean()
    is_garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("west", "West"),
            ("east", "East"),
        ],
    )
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner")
    seller_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id")
    total_area = fields.Float(compute="_compute_area", store=True)
    best_price = fields.Float(
        compute="_compute_best_price", string="Best Offer", store=True
    )

    @api.depends("offer_ids")
    def _compute_best_price(self):
        max = 0
        for record in self.offer_ids:
            max = record.price if record.price > max else max
        self.best_price = max

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("is_garden")
    def _onchange_is_garden(self):
        if self.is_garden is True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def property_sold(self):
        for record in self:
            if record.status == "canceled":
                raise UserError("sold properties cannot be canceled!")
            record.status = "sold"

    def property_canceled(self):
        for record in self:
            if record.status == "sold":
                raise UserError("Canceled properties cannot be sold!")
            record.status = "canceled"
