from odoo import api, models, fields
from datetime import date, timedelta
from odoo.exceptions import UserError


class Testing(models.Model):
    _name = "estate.property"
    _description = "This is Real Estate"

    name = fields.Char('property Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date availability', copy=False, default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float('expected price', required=True)
    selling_price = fields.Float('sell price', readonly=True, copy=False)
    bedrooms = fields.Integer('bedrooms', default=2)
    living_area = fields.Integer('live area')
    facades = fields.Integer('facades')
    garage = fields.Boolean('garage')
    garden = fields.Boolean('garden')
    garden_area = fields.Integer('garden area')
    garden_orientation = fields.Selection(
        string='Garden direction',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    state = fields.Selection(
        string='state',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        default='new',
        copy=False
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        inverse_name="property_id",
        string="property name"
    )
    salesperson_id = fields.Many2one("res.users", string="Sales person", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="property offer")

    total_area = fields.Float(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(string="Best Offer Price", compute="_compute_best_price")

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            raise UserError("A canceled property cannot be set as sold")

    def action_sold(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            raise UserError("A sold property cannot be canceled.")
