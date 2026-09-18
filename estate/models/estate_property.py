from odoo import models, fields, api


class Property(models.Model):
    _name = "estate_property"
    _description = "estate property model"

    name = fields.Char('Nom', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Date Availability', copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Prince', readonly=True, copy=False)
    bedrooms = fields.Integer('# Bedrooms', default=2)
    living_area = fields.Integer('# Living Areas')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean('Has Garage')
    garden = fields.Boolean('Has Garden')
    garden_area = fields.Integer('# Garden Areas')
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
        ('north', "North"),
        ('south', "South"),
        ('east', "East"),
        ('west', "West"),
        ]
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default='new',
    )

    salesperson = fields.Many2one('res.users', string="Salesperson", index=True, default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string="Buyer", copy=False)

    tag_ids = fields.Many2many('estate_property.tag', string="Tags")

    offer_ids = fields.One2many('estate_property.offer', 'property_id', string="Offer")

    total_area = fields.Integer(compute="_compute_areas")

    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_areas(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped(("price")))
