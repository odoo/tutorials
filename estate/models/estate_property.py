from dateutil.relativedelta import relativedelta

from odoo import api, models, fields
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real estate property"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda x: fields.Datetime.today() + relativedelta(months=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute='_compute_total_area')
    garden_orientation = fields.Selection([
        ('north', "North"),
        ('south', "South"),
        ('east', "East"),
        ('west', "West"),
    ])

    state = fields.Selection([
        ('draft', "New"),
        ('received', "Offer Received"),
        ('accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancel', "Cancelled"),
    ], string="Status", copy=False, default='draft', required=True)

    property_type_id = fields.Many2one(comodel_name="estate.property.type")
    buyer_id = fields.Many2one(comodel_name="res.partner", copy=False)
    salesperson_id = fields.Many2one(comodel_name="res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id")
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_has_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = None
            self.garden_area = 0.0

    def set_to_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("You can't cancel sold properties")
            record.state = 'cancel'
        return True

    def set_to_sold(self):
        for record in self:
            if record.state == 'cancel':
                raise UserError("You can't sell cancelled properties")
            record.state = 'sold'
        return True
