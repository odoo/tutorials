from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')

    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Saleswoman', default=lambda self: self.env.user)

    tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
            'Availale From',
            copy=False,
            default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living area (m²)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden area (m²)')
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Garden orientation in respect to main compass directions")
    active = fields.Boolean(default=True)
    state = fields.Selection(
            selection=[
                ('new', 'New'),
                ('offer_received', 'Offer Received'),
                ('offer_accepted', 'Offer Accepted'),
                ('sold', 'Sold'),
                ('cancelled', 'Cancelled')],
            default='new',
            help="State of the estate property")

    total_area = fields.Integer(
            'Total area (m²)',
            compute='_compute_total_area',
            help='Total area of the estate defined as a sum of living and garden area')

    best_price = fields.Float(
            'Best Offer',
            compute='_compute_best_price',
            help='Best offer from the availale offers or zero')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        if len(self.offer_ids) == 0:
            for record in self:
                record.best_price = 0.0
        else:
            for record in self:
                record.best_price = min([offer.price for offer in record.offer_ids])

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = None

    def action_set_property_as_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_("Estate property can not be marked as sold if it was cancelled"))

            record.state = "sold"

            return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Estate property can not be marked as cancelled if it was already sold"))

            record.state = "cancelled"

            return True
