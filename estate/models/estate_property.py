from odoo import fields, models, api


class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties"

    active = fields.Boolean(default=True)
    bedrooms = fields.Integer(default=2)
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    description = fields.Text()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ]
    )
    living_area = fields.Integer()
    name = fields.Char(required=True)
    postcode = fields.Char()
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    selling_price = fields.Float(readonly=True, copy=False)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer received', "Offer Received"),
            ('offer accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Canceled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    sales_person = fields.Many2one(
        "res.users", string="Sales Person", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    total_area = fields.Float(
        compute="_compute_total_area", string="Total Area", store=True
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = False
