from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    Property_Type = fields.Text()
    description = fields.Text()
    postcode = fields.Char()
    state = fields.Text()
    date_availability = fields.Date(copy=False, readonly=True, default=lambda self: date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (m2)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (m2)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),
        ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    status = fields.Selection(
    copy=False,
    readonly=True,
    default='new',
    string='Status',
    selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')]
    )

    def action_set_sold(self):
        if (self.state != "Cancelled"):
            self.state = "Sold"
        else:
            raise UserError("A cancelled property can not be sold")
        return True

    def action_set_cancelled(self):
        if (self.state != "Sold"):
            self.state = "Cancelled"
        else:
            raise UserError("A sold property can not be cancelled")
        return True

    Property_Type_id = fields.Many2one('estate.property.type', string='Type')
    Buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    Salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    tags_ids = fields.Many2many('estate.property.tags', string='Tags')
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="offer")
    total_area = fields.Integer(string='Total Area(m2)', compute='_compute_total_area', store=True)
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price', store=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + (property.garden_area or 0)

    @api.depends('offer_ids.price')
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
            self.garden_orientation = False
