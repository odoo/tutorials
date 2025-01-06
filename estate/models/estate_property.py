# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _ #importing _ for the text of the error(unsure).
from odoo.exceptions import UserError, ValidationError #importing to throw error in ui view
from dateutil.relativedelta import relativedelta # to do operation on datetime class.
import odoo.tools.float_utils as floatUtil


class EstateProperty(models.Model):
    
    _name = "estate.property"
    _description = "Estate property"
    _order= "id desc"
    
    name = fields.Char('Name', required=True)
    description= fields.Text('Property Description')
    postcode= fields.Char("Postcode")
    date_availability=fields.Date(string="Date Availability", copy=False, default=fields.Date.today() + relativedelta(months=+3))
    
    expected_price=fields.Float("Expected price", required=True)
    selling_price=fields.Float(string="Selling price", readonly=False, copy=False)
    best_price= fields.Float(string="Best Offer", compute="_compute_best_price", help="takes the biggest prices offered for this property")
    
    bedrooms= fields.Integer("Bedrooms", default=2)
    living_area= fields.Integer("Living Area(sqm)")
    facades= fields.Integer("Facades")
    garage= fields.Boolean("Garage")
    garden= fields.Boolean("Garden")
    garden_area= fields.Integer("Garden Area(sqm)")
    garden_orientation= fields.Selection(
        selection=[ 
            ("east", "East"), #(value, label)
            ("west", "West"),
            ("north", "North"),
            ("south", "South")
        ],
        string="Garden Orientation",
        help="Orientation can be East, West, North, South Only" #help to be shown in the view as ?
    )
    
    # below active and state field is a reserved fields
    active= fields.Boolean(string="Active", default=True) #available
    state= fields.Selection(
        string='Status',
        default='new', #need to define the value not a label 
        selection=[
            ('new', 'New'), 
            ('offer_received', 'Offer Received'), 
            ('offer_accepted', 'Offer Accepted'), 
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True
    )
    
    property_type_id= fields.Many2one(comodel_name="estate.property.type",string="Property Type")   
    buyer= fields.Many2one(comodel_name="res.partner",string="Buyer", copy=False) #partner person can be     company, an individual or even a contact address.
    tag_ids= fields.Many2many(comodel_name="estate.property.tag", string="Tags")
    salesperson= fields.Many2one(comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user) #default value is self.env.user is the current user’s record

    offer_ids= fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id") #inverse_name refers to the foreign field of model
    #? there will be always one2many mapping for all the many2one mapping in another table, always define the inverse_name(foriegn field) in the one2many mapping
    #? inverse method is called when saving the record, while the compute method is called at each change of its dependencies.
    total_area= fields.Integer(string="Total Area(sqm)", compute="_compute_total_area", help="Total Area is the sum of Living Area and Garden Area")
    #? since the store!=True the above field is not going to store in the db

    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_not_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("Only new and cancelled property can be deleted")
    
    
    _sql_constraints = [
        ('expected_price_check', 'CHECK(expected_price>=0.0)', 'Expected price must be positive'),
        ('selling_price_check', 'CHECK(selling_price>0.0 or selling_price=null)', 'Selling price must be positive')
    ]
    
    @api.constrains('selling_price', 'expected_price') #python constraints
    def _check_selling_price_not_to_be_less_90_per_of_expected_price(self):
        for records in self:
            if(floatUtil.float_is_zero(value=records.selling_price, precision_digits=2)):
                continue
            else:
                #90% of expected price
                per_90_of_expected_price= records.expected_price * (90/100)
                if(floatUtil.float_compare(value1=records.selling_price, value2=per_90_of_expected_price, precision_digits=2) == -1):
                    raise ValidationError(_("The selling price cannot be lower than 90% of the expected price"))
    
    
    # @api.onchange("offer_ids")
    # def update_offer_state(self):
    #     for record in self:
    #         if(len(record.offer_ids)>0 and record.state=="new"):
    #             record.state="offer_received"            
    
    
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area= record.living_area + record.garden_area
     
     
    @api.depends('offer_ids.price')
    def _compute_best_price(self): #getting the max price from the offered price
        for record in self:
            print(record.offer_ids.mapped('price'),"?????????????")
            record.best_price= max(record.offer_ids.mapped('price'), default=0) #The filtered will return the recordsets that match the criteria or condition. The Mapped function,it returns a set of field values. Its argument accepts a string value as the column name and returns all the possible values from the recordset.
    

    @api.onchange('garden')
    def garden_value_change(self):
        #we do not loop on self, this is because the method is only triggered in a form view
        if(self.garden):
            self.garden_area=10
            self.garden_orientation='north'
        else:
            self.garden_area=0
            self.garden_orientation=None
            
        
    #method triggering from form view on click of button sold in estate property    
    def mark_property_sold(self):
        for record in self:
            if(record.state == 'cancelled'):
                raise UserError(_("Cancelled property cannot be sold."))
            record.state='sold'
        return True #a public method should always return something so that it can be called through XML-RPC. When in doubt, just return True.
    
    #method triggering from form view on click of button cancelled in estate property 
    def mark_property_cancel(self):
        for record in self:
            if(record.state == 'sold'):
                raise UserError(_("Sold property cannot be cancelled."))
            record.state='cancelled'
        return True #a public method should always return something so that it can be called through XML-RPC. When in doubt, just return True.
        