from odoo import api, models, fields
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char("Estate Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postalcode")
    date_availability = fields.Date('Date Availability', default=lambda self: date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(selection=[
        ('north', 'NORTH'),
        ('south', 'SOUTH'),
        ('west', 'WEST'),
        ('east', 'EAST')
        ])
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(selection=[
        ('new', 'NEW'),
        ('offer_received', 'OFFER RECEIVED'),
        ('offer_accepted', 'OFFER ACCEPTED'),
        ('sold', 'SOLD'),
        ('cancelled', 'CANCELLED')
        ], default='new')
    property_type_id = fields.Many2one('estate.property.type', string='Real Estate Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.partner', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Real Estate Tag')
    offer_ids = fields.One2many('estate.property.offer', inverse_name='property_id')
    total_area = fields.Float('Total Area (sqm)', compute='_compute_total_area', readonly=True)
    best_offer = fields.Float('Best Offer', compute='_compute_best_offer', readonly=True)
    _order = 'id desc'

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0)',
         'The expected price should be strictly greater than 0.'),
        ('selling_price', 'CHECK(selling_price >= 0)',
         'The selling price should be zero or strictly greater than 0 if an offer is accepted.'),
        ]

    def action_reset_to_draft(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("You cannot reset a sold property to draft.")
            record.state = 'new'

    def action_open_offers(self):
        self.ensure_one()
        return {
            'name': 'Property Offer',
            'views': [(self.env.ref('estate.estate_property_offer_view_list').id, 'list')],
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.offer_ids.ids)],
            'res_model': 'estate.property.offer'
        }

    def action_cancel(self):
        if self.state != 'cancelled':
            self.state = 'cancelled'

    def action_sold(self):
        if self.state == 'cancelled':
            raise UserError("You can't sold an estate marked as CANCELLED")
        self.state = 'sold'

    @api.ondelete(at_uninstall=False)
    def on_delete(self, vals_list):
        for val in vals_list:
            if val and val['state'] == 'new' or val['state'] == 'cancelled':
                raise UserError('You can not delete a new or cancelled property')

    @api.constrains('expected_price', 'selling_price')
    def _check_expected_price(self):
        for record in self:
            if float_compare(record.expected_price * 0.9, record.selling_price, 3) == 1 and record.selling_price != 0:
                raise ValidationError("The selling price must be at least the 90% of the expected price.")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + (record.garden_area or 0)

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(offer.price for offer in record.offer_ids)
            else:
                record.best_offer = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None
