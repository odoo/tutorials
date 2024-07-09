from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real_Estate property model"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available Data', copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='state',
        selection=[('new', 'New'), (' offer received', ' Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'),
                   ('cancelled', ' Cancelled')],
                   default='new',
                required=True,
                copy=False
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    user_id = fields.Many2one("res.users", string="salesperson")
    partner_id = fields.Many2one("res.partner", string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="offers")

    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Integer(compute="_compute_highest")

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_highest(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_set_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("cancelled property cannot be sold")
            record.state = "sold"
        return True

    def action_set_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError('sold property cannot be cancelled.')
            record.state = "cancelled"
