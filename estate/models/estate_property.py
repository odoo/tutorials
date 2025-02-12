from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, exceptions, _


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate properties"
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'), 
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be positive.')
    ]

    name = fields.Char('Title', required=True, translate=True)
    tags_ids = fields.Many2many(
        comodel_name='estate.property.tag', string='Tags')
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one(
        comodel_name='res.users', string='Salesman', 
        default=lambda self: self.env.user)
    buyer_id = fields.Many2one(
        comodel_name='res.partner', string='buyer_id', 
        copy=False)
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer', 
        inverse_name='property_id')
    description = fields.Text('Description')
    postcode = fields.Char('Postcode', required=True)
    date_availability = fields.Date('Available From', copy=False, 
        default = fields.Datetime.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    best_offer = fields.Float('Best Offer', 
        compute="_compute_best_offer")
    bedrooms = fields.Integer('Bedrooms', default="2")
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    total_area = fields.Integer('Total Area (sqm)', 
        compute="_compute_total_amount")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')],
        help="Defines the orientation of the garden")
    active = fields.Boolean('Active', default="True")
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'),
        ('offer received', 'Offer Received'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')],
        help="Status of the Property",
        required=True, copy=False,
        default="new")

    @api.depends("living_area", "garden_area")
    def _compute_total_amount(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.mapped('offer_ids.price'), default=0)
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            threshold_price = 0.9 * record.expected_price  
            low_selling_price = record.selling_price <= threshold_price  
            low_best_offer = record.best_offer <= threshold_price  
            has_offers = len(record.offer_ids) > 0
            if (low_selling_price or low_best_offer) and has_offers:
                raise exceptions.ValidationError("The selling price must be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer.")

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        elif self.garden == False:
            self.garden_area = None
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_is_new_or_cancelled(self):
        for record in self:
            if record.state in ['offer received', 'offer accepted', 'sold']:
                raise exceptions.UserError("Only new and cancelled properties can be deleted.")

    def action_sell_property(self):
        for record in self:
            record.state = "sold"
        return True
    
    def action_cancel_property(self):
        for record in self:
            record.state = "cancelled"
        return True
