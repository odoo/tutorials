from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: (date.today() + relativedelta(months=3)).strftime('%Y-%m-%d'),
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(default=True)
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('east', 'East'), ('west', 'West'), ('south', 'South')],
                                          required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('cancelled', 'Cancelled')], default='new', string='Status')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    user_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(compute='_compute_total_area', store=True)
    best_price = fields.Float(
        string='Best Offer',
        compute='_compute_best_price',
        store=True,
        readonly=True
    )
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'Expected price must be positive!'),
        ('check_selling_price_positive', 'CHECK(selling_price > 0)', 'Selling price must be positive!'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            best_offer = max(record.offer_ids.mapped('price'), default=0)
            record.best_price = best_offer

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Property is cancelled. No further actions can be taken on this property.")
            accepted_offers = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            if not accepted_offers:
                raise UserError("Property must be in 'Accepted' state before it can be sold.")
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Property is already sold. No further actions can be taken on this property.")
            record.state = 'cancelled'

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.selling_price < record.expected_price * 0.9:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("You cannot delete a property that is not in 'New' or 'Cancelled' state.")
