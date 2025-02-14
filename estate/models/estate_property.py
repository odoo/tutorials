from odoo import fields,models,api
from odoo.tools import float_compare,float_is_zero
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description =" Good real estate"
    _order="id desc"

    name= fields.Char(required=True)
    description=fields.Text()
    postcode=fields.Char()
    date_availability = fields.Date(default= datetime.now() + timedelta(days=90))
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    garden_area=fields.Integer()
    total_area= fields.Integer(compute='_compute_total_area')
    facades=fields.Integer()
    garage= fields.Boolean()
    garden= fields.Boolean()
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True,
        default=lambda self: self.env.company
    )
    garden_orientation= fields.Selection(string='Garden orientation',
        selection=[
            ('North', 'North'),
            ('West', 'West'),
            ('South', 'South'),
            ('East', 'East')
        ]
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True,
        default='new',
        copy=False
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string='Offers')
    best_price= fields.Float(compute='_compute_best_price')
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', copy=False, string='Buyer')
    property_tags_ids=fields.Many2many('estate.property.tag')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]

    @api.depends('garden_area','living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area= record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price= max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'North'
            else:
                record.garden_area = 0
                record.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Property is already cancelled, you cannot sell this property.")
            accepted_offers = record.offer_ids.filtered(lambda offer: offer.status == 'Accepted')
            if not accepted_offers:
                raise UserError("You cannot sell this property without at least one accepted offer.")
            record.state = 'sold'
        return True

    def action_cancelled(self):
        for record in self:
            if record.state=='sold':
                raise UserError("Property is already sold ,it cannot be cancelled")
            else:
                record.state='cancelled'
        return True

    @api.constrains('expected_price', 'selling_price')
    def _check_offer_price_slab(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_acceptable_price= 0.9*record.expected_price
            if float_compare(record.selling_price,min_acceptable_price, precision_digits=2)==-1:
                raise UserError(
                    "Selling price must be greater than 90% of expected price. It should be more than {:.2f}".\
                    format(min_acceptable_price)
                )

    @api.ondelete(at_uninstall=False)
    def property_deletion(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("You can only delete properties in the 'New' or 'Cancelled' state.")
