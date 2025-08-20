from odoo import api,fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"



    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availaility = fields.Date(default=(fields.Date.add(fields.Date.today(), days=90)), copy=False)
    
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly = True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Type',
        selection=[('North','north'),('South','south'),('East','east'),('West','west')],
        help="Type is used to know the direction of the Garden ")
    active = fields.Boolean(default = True)
    state = fields.Selection([   ('new', 'New'),
    ('offer_received', 'Offer Received'),
    ('offer_accepted', 'Offer Accepted'),
    ('sold', 'Sold'),
    ('cancelled', 'Cancelled'),],required=True, copy=False, default='new')
    property_type = fields.Many2one("estate.property.type", string="Property Type")
    salesman = fields.Many2one("res.users", default = lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offers_ids = fields.One2many("estate.property.offers", "property_id")
    total_area = fields.Integer(compute= "_compute_area")
    best_price = fields.Float(compute="_compute_bestprice")

    #it's calculate the total area
    @api.depends('living_area','garden_area')
    def _compute_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    #it's taking the best offer from among all
    @api.depends('offers_ids.price')
    def _compute_bestprice(self):
        for record in self:
            record.best_price = max(record.offers_ids.mapped('price'), default = 0)
    
    #change the values on the basis of the garden True or False
    @api.onchange('garden')
    def _onchnage_garden(self):
        if self.garden==True:
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area = 0
            self.garden_orientation = ""


