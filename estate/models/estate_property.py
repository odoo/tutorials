from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    def caluate_date(self):
        return fields.Date.today() + relativedelta(months=3)

    date_availability = fields.Date(default=caluate_date)

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char(required=True)
    expected_price = fields.Float(required=True, default=False)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    selling_price = fields.Float(copy=False)
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        copy=False,
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
        ],
        copy=False,
    )
    buyer = fields.Many2one("res.partner", copy=False)

    salesperson = fields.Many2one("res.users", default=lambda self: self.env.user)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many(
        "estate.property.tag",
        column1="estate_property_id",
        column2="estate_property_tag_id",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")

    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = False

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
