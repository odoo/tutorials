from odoo import fields, models, api
import datetime


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property model test description"

    total_area = fields.Integer(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        self.total_area = self.garden_area + self.living_area

    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    name = fields.Char(required=True)
    description = fields.Text("Description of the Estate Propert Model")
    postcode = fields.Char("Post code")
    date_availability = fields.Date(
        "Availability date",
        default=lambda self: datetime.date.today() + datetime.timedelta(days=90),
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
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
            ("west", "West"),
            ("east", "East")
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Property Offers")
