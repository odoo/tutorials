from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3), string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[
                ('north', 'North'),
                ('west', 'West'),
                ('south', 'South'),
                ('east', 'East')
            ],
        help="Choose the appropriate orientation of the garden"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Estate status",
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        help='This field explain the estate status.',
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    seller_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user, domain="[('type', '=', 'internal')]")
    buyer_id = fields.Many2one("res.partner", string="Buyer", domain="[('type', '=', 'portal')]")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_offer", string="Best Offer")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if len(record.offer_ids) > 0 else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if not record.garden:
                record.garden_area = 0
                record.garden_orientation = ''
            else:
                record.garden_area = 10
                record.garden_orientation = 'north'
