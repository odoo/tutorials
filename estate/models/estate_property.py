from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Propety"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available Date",
        default=lambda self: (fields.Date.today() + relativedelta(months=3)),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("North", "north"),
            ("South", "south"),
            ("East", "east"),
            ("West", "west"),
        ],
        help="Type is used For garden_orientation",
    )
    active = fields.Boolean()
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="new",
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )

    total_area = fields.Float(string="Total Area", compute="_compute_total_area")

    best_offer = fields.Float(
        string="Best Area",
        compute="_compute_best_offer",
        store=True,
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + (property.garden_area or 0)

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            best_offer = max(property.offer_ids.mapped("price"), default=0)
            property.best_offer = best_offer
