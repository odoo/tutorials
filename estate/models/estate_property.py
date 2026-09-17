from odoo import api, fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    postcode = fields.Char()
    description = fields.Text()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
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
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="The garden orientation",
    )
    total_area = fields.Integer(compute="_compute_total_area")
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        copy=False,
        required=True,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tags_ids = fields.Many2many("estate.property.tag")
    buyer = fields.Many2one("res.partner", copy=False)
    salesman = fields.Many2one("res.users", default=lambda self: self.env.user)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.depends("living_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
