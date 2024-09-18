from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties"

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new', required=True, copy=False
    )

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    total_area = fields.Integer(compute='_compute_total_area')

    property_type_id = fields.Many2one('estate.property.type')

    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False, readonly=True)
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = 0
            if rec.offer_ids:
                rec.best_price = max(rec.offer_ids.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_set_as_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("Cannot sell a canceled property"))
            record.state = 'sold'
        return True

    def action_set_as_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("Cannot cancel a sold property"))
            record.state = 'cancelled'
        return True

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive'),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for rec in self:
            print("rec.state", rec.state)
            print("rec.selling_price", rec.selling_price)
            print("rec.expected_price", rec.expected_price)
            if rec.state == 'sold' and float_compare(rec.selling_price, rec.expected_price * 0.9, precision_digits=2) < 0:
                raise UserError(_("The selling price must be at least 90% of the expected price."))
