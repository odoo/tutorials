from odoo import fields, models,api,exceptions
from dateutil.relativedelta import relativedelta


class Property_Plan(models.Model):



    _name = "estate.property"
    _description = "Custom model for real estate."
   
    name = fields.Char(required=True,string="Title")

    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    #One2Many
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="OfferID")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer',copy=False)

    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3) ,string="Available From")
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[("north","North"), ("south","South"),("east","East"),("west","West")],
        help="Type is used for direction"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ],required=True,copy=False,default='new')

    total_price = fields.Float(string="Total Area", compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_price = record.living_area + record.garden_area

    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store=True)
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"),default=0)
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'  
        else:
            self.garden_area = 0
            self.garden_orientation = None
    
    def action_set_cancel(self):
        for record in self:
            if(record.state == 'sold'):
                raise exceptions.UserError("Sold properties can't be canceled")
            else:
                record.state= 'cancelled'
        return True
    
    def action_set_sold(self):
        for record in self:
            if(record.state == 'cancelled'):
                raise exceptions.UserError("Canceled properties can't be sold")
            else:
                record.state = 'sold'
        return True
