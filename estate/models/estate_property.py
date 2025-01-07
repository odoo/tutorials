
from odoo import models,fields,api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Management Module"
    _order= "id desc"

    name = fields.Char('Property Name', required=True)
    description=fields.Text('Description' )
    postcode = fields.Char('Postcode')
    date_availability=fields.Date( 'Available From', copy=False, default= (datetime.today() + relativedelta(months=3)).date())
    
    
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)

    bedrooms = fields.Integer('Bedrooms', default=2)
    bedrooms = fields.Char('Bedrooms', default='two')

    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')

    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection( 
                selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
                string='Garden Orientation') 

    active=fields.Boolean(default=True)
    # last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)


    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string='State',
        required=True,
        default='new',  
        copy=False,  
    )

    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type", auto_join=True, ondelete="cascade")
    
    user_id = fields.Many2one('res.users', string='Salesman', index=True, default=lambda self: self.env.user, ondelete="cascade")
    partner_id = fields.Many2one('res.partner', string='Buyer', index=True, ondelete="cascade")

    tag_ids=fields.Many2many(comodel_name="estate.property.tag", string="Property Tags", ondelete="cascade" )

    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',  
        inverse_name='property_id',  
        string='Offers' , 
        ondelete="cascade"
    )
    
    
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")


    @api.depends("garden_area","living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if not record.offer_ids:
                record.best_price=0
                continue
            record.best_price = max(record.offer_ids.mapped('price'))

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation=None
        else:
            self.garden_area=10
            self.garden_orientation='north'


    status_button=fields.Char()

    def sell_action(self):
        for record in self:
            if record.status_button != 'cancelled':
                record.status_button= 'sold'
                record.state='sold'
            else:
                raise UserError("CANCELLED properties can not be SOLD")
                
                
        return True

    def cancel_action(self):
        for record in self:
            if record.status_button != 'sold':
                record.status_button='cancelled'
                record.state='cancelled'
            else:
                raise UserError("SOLD properties can not be CANCELLED")
                
            
        return True
    

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be strictly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price must be non-negative",
        ),
    ]
     
    
    
    estate_id = fields.Many2one("estate.property.type")
    
    # @api.constrains('offer_ids')
    # def _check_offer_received(self):
    #     for record in self:
    #         if record.offer_ids:
    #             if record.state=='new':
    #              record.state='offer_received'
    #         else:
    #             record.state='new'
    
        
    #     return True
    

    @api.ondelete(at_uninstall=False)
    def _unlink_except_state_new_cancelled(self):
        for record in self:
            if record.state == 'offer_accepted' or record.state=='sold' or record.state=='offer_received':
                                raise UserError("Can't delete this Record")

      
     

    

