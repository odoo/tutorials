from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
        string="Available From"
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        default='new',
        copy=False
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type'
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Property Tags'
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers'
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute='_compute_total_area'
    )
    best_price = fields.Float(
        string="Best Offer",
        compute='_compute_best_price'
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids) > 0:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = None

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = None
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'

    def action_set_to_sold(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise UserError("You cannot sell a canceled property")
        return True

    def action_set_to_canceled(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise UserError("You cannot cancel a sold property")
        return True
