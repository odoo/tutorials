from odoo import api, models, fields


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
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
    total_area = fields.Float(compute="_compute_total_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False
