from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property description"
    _order = "id desc"

    name = fields.Char('Estate Name', required=True)

    property_type_id = fields.Many2one('estate.property.type', string='Property type')
    partner_id = fields.Many2one('res.partner', string='Buyer')
    user_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)

    tags_ids = fields.Many2many('estate.property.tag', string='Tags')


    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    total_area = fields.Integer(compute="_compute_total_area")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Integer(compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            best_price = 0

            for offer in record.offer_ids:
                best_price = max(best_price, offer.price)
            
            record.best_price = best_price


    active = fields.Boolean('Active', default=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability', copy=False, default=fields.Date.today() +  relativedelta(month=4))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Number of Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Number of Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')])

    state = fields.Selection(
        selection=[
            ('new', 'New'), 
            ('offer_received', 'Offer Received'), 
            ('offer_accepted', 'Offer Accepted'), 
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')], default="new", required=True, copy=False)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area=10
            self.garden_orientation="north"
        else:
            self.garden_area=0
            self.garden_orientation=False

    def sold_button_action(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError('Cancelled property cannot be sold')
            record.state = "sold"

    def cancel_button_action(self):
        for record in self:
            if record.state == "sold":
                raise UserError('Sold property cannot be cancelled')
            record.state = "cancelled"

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(f"You cannot delete the property {record.name} unless its state is 'New' or 'Cancelled'.'")

    _sql_constraints = [
        ('check_positive_price', 'CHECK(expected_price >= 0)',
         'The expected price of a real estate should always be positive'),
         ('check_positive_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price of a real estate should always be positive')
    ]
    