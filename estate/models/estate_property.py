from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="living area(sqm)")
    facades = fields.Integer()
    active = fields.Boolean(default=True)
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden area(sqm)")
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
        help="Direction the garden faces"
    )
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)

    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)
