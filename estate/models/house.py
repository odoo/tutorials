from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils

class House(models.Model):
    _name = 'estate.house'
    _description = 'House Model'
    _sql_constraints = [
        ('check_positive_expected_price', 'CHECK(expected_price > 0)', "expected_price can't be negative"),
        ('check_positive_selling_price', 'CHECK(selling_price > 0)', "selling_price can't be negative")
    ]
    _order = 'id desc'

    name = fields.Char(string='House Name', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self : self.get_availability_date())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[
        ('s', 'South'),
        ('n', 'North'),
        ('w', 'West'),
        ('e', 'East')
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status', 
        readonly=True,
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ], 
        default='new',
        required=True)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    seller_id = fields.Many2one('res.users', string='Salesperson')
    house_type_id = fields.Many2one('estate.house.type', string='Property Type')
    house_tag_ids = fields.Many2many('estate.house.tag')
    offer_ids = fields.One2many('estate.house.offer', 'property_id')
    total_area = fields.Float(compute='_calculate_total_area')
    best_price = fields.Float(compute='_calculate_best_price')
    
    def get_availability_date(self):
        current_date = fields.Date.today()
        return fields.Date.add(current_date, month=3)
    
    @api.depends("living_area", "garden_area")
    def _calculate_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _calculate_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if(self.garden):
            self.garden_area = 100
            self.garden_orientation = 'N'
        else:
            self.garden_area = 0
            self.garden_orientation = None
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_not_new_or_cancelled(self):
        for house in self:
            if(not house.state in ('new', 'cancelled')):
                raise UserError(f"Can't delete {house.state} state house")

    def sell_property(self):
        for house in self:
            if(house.state == 'cancelled'):
                raise UserError("Cancelled property can't be sold")
            house.state = 'sold'
    
    def cancel_property(self):
        for house in self:
            if(house.state == 'sold'):
                raise UserError("Sold property can't be cancelled")
            house.state = 'cancelled'

    @api.constrains("selling_price", "expected_price")
    def _check_selling_expected_price_constraint(self):
        for house in self:
            if(not house.state == 'offer_accepted'):
                return
            threshold = 0.9 * house.expected_price
            if(float_utils.float_compare(house.selling_price, threshold, precision_digits=2) == -1):
                raise ValidationError("selling_price can't be less than 90% of the expected_price")
