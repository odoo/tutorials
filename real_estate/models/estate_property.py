from odoo import models, fields, api
from odoo.exceptions import UserError  
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate"
    _inherit = ['mail.thread']
    _order = "id desc"   

    name = fields.Char(required=True)
    image = fields.Binary()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True , copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garden = fields.Boolean()
    garage = fields.Boolean()
    garden_area = fields.Integer()
    
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(string="Best Offer Price",  store=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'),('east', 'East'),('west','West')],
         help="Type is used to separate Leads and Opportunities")

    state = fields.Selection([
    ('new', 'New'),
    ('offer_received', 'Offer Received'),
    ('offer_accepted', 'Offer Accepted'),
    ('sold', 'Sold'),
    ('cancelled', 'Cancelled')  
], string="Status", default="new")
    
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson" , default=lambda self: self.env.user)
    tag_id = fields.Many2many("estate.property.tag", string="Tags")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")


    total_area= fields.Float(compute="_compute_total_area", readonly=True, copy=False)
    best_price= fields.Float(compute="_compute_best_price", readonly=True, default= 0.0)

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price > 0 )', 'A property selling price must be positive'),
        ('check_expected_price', 'CHECK(expected_price > 0 )', 'A property expected price must be strictly positive')
    ]

    @api.constrains('selling_price')
    def check_selling_price(self):
       if self.state == "accept" and self.selling_price < (0.90 * self.expected_price):
            raise UserError("selling price cannot be lower than 90% of the expected price.")


    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        self.total_area=self.living_area +self.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)


    @api.onchange("garden")
    def _change_garden(self):
        if(self.garden):
            self.garden_area=10
            self.garden_orientation="north"
        else:
            self.garden_area=False
            self.garden_orientation=False

    def action_sold(self):
        if self.state != "cancelled" and self.state == "offer_accepted" :
            self.state = "sold"

        elif self.state != "offer_accepted":
            raise UserError("without offer accept properties cannot be set as Sold")
            
        else:
            raise UserError("Cancelled properties cannot be set as Sold")
        return True

    def action_cancel(self):
        if self.state != "sold":
            self.state = "cancelled"
            self.offer_ids.state = "refused"
        else:
            raise UserError("Sold properties cannot be set as cancelled")

    @api.ondelete(at_uninstall=False)
    def _prevent_deletion(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("You can only delete properties that are 'New' or 'Cancelled'.")    

    
    def action_estate_add_offer_wizard(self):
      return {
        'name': 'Add Offer',
        'type': 'ir.actions.act_window',
        'res_model': 'estate.add.offer.wizard',
        'view_mode': 'form',
        'target': 'new',
        'context': {'default_property_ids': self.ids},
    }
