from odoo import api, fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    living_area = fields.Integer()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute='_compute_total_area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
        ],
        help='Orientation of the garden')
    state = fields.Selection(
        string='Status',
        selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one('property.type', string='Property Type')
    tag_ids = fields.Many2many('property.tag', string='Property Tags')
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    offer_ids = fields.One2many('property.offer', 'property_id', string='Offers')
    # best_price = fields.Float(compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # @api.depends('offer_ids.price')
    # def _compute_best_price(self):
    #     for record in self:
    #         if record.offer_ids:
    #             record.best_price = max(record.offer_ids.mapped('price'))
    #         else:
    #             record.best_price = 0.0
