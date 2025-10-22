from odoo import fields, models, api, exceptions
from odoo.tools.date_utils import add


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate propreties"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda x: add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new', copy=False, required=True)
    seller_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner')
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute="_compute_total_area", readonly=True, copy=False)
    best_price = fields.Float(compute="_get_best_price", readonly=True, copy=False)
    is_available = fields.Boolean(compute='_compute_is_available')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _get_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_set_sold(self):
        if self.state == 'cancelled':
            raise exceptions.UserError("Cancelled property cannot be set as sold")
        self.state = 'sold'
        return 1

    def action_set_cancelled(self):
        if self.state == 'sold':
            raise exceptions.UserError("Sold property cannot be cancelled")
        self.state = 'cancelled'
        return 1

    @api.depends('offer_ids.status')
    def _compute_is_available(self):
        for record in self:
            record.is_available = not any(s == 'accepted' for s in record.offer_ids.mapped('status'))
