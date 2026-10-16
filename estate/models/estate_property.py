from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, string="Available From", default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(selection=[
        ('north', "North"),
        ('south', "South"),
        ('east', "East"),
        ('west', "West"),
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[
        ('new', "New"),
        ('offer_received', "Offer Received"),
        ('offer_accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancelled', "Cancelled"),
    ], required=True, default='new', copy=False)
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string="Tags", copy=False)
    total_area = fields.Integer(string="Total Area (sqm)", compute='_compute_total_area')

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer = fields.Many2one('res.partner', string="Buyer")
    salesman = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)

    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    best_price = fields.Float(string="Best Offer", compute='_compute_best_price')

    # ------------------------------------------------------------
    # COMPUTED FIELDS
    # ------------------------------------------------------------

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price')) if property.offer_ids else 0.0

    # ------------------------------------------------------------
    # ONCHANGES
    # ------------------------------------------------------------

    @api.onchange("garden")
    def _onchange_garden(self):
        self.ensure_one()
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = 0
