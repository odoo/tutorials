from odoo import api,models,fields
from datetime import date , timedelta


class EstateProperty(models.Model):
    _name = "estate.property" 
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    expected_price = fields.Float(string="Expected Price", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From",copy=False,default=lambda self: date.today() + timedelta(days=(90)))
    selling_price = fields.Float(string="Selling Price",readonly=True,copy=False)
    bedrooms = fields.Integer(string="Bedrooms",default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    active = fields.Boolean(default=True)
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation")

    state = fields.Selection([
        ('new', 'New'),('offer_received', 'Offer Received'),('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),('cancelled', 'Cancelled'),],
        string="State", required=True, default='new', copy=False)
    
    # many2one
    property_type_id = fields.Many2one("estate.property.type",string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users",string="Salesman",default=lambda self: self.env.user)
    
    #many2one 
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    #one2many
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # total Area
    total_area = fields.Float(compute="_compute_total_area", store=True , string="Total Area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # best_price
    best_offer = fields.Float(compute="_compute_best_offer", store=True)

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            # Using mapped() to get all offer prices and then find the maximum
            record.best_offer = max(record.offer_ids.mapped("price"), default=0.0)

    