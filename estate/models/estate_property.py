from odoo import api,fields, models
from datetime import date, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "reals estate properties"

    name = fields.Char('Property Name',required=True)
    offer_ids=fields.One2many("estate.property.offer","property_id",string="Offers Received")
    tag_ids=fields.Many2many("estate.property.tags",string="Tags")
    buyer_id=fields.Many2one("res.partner",string="Buyer")
    salesperson_id=fields.Many2one("res.users",string="Sales Person",default=lambda self: self.env.user)
    property_type_id = fields.Many2one("estate.property.types", string="Property Type")
    description = fields.Text('The Descritption')
    postcode = fields.Char()
    date_availability = fields.Date(default=date.today()+ timedelta(days=90),copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False,readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area= fields.Integer()
    garden_orientation = fields.Selection([("North","North"),("South","South"),("East","East"),("West","West")])
    active = fields.Boolean(default=True)
    state = fields.Selection([("New","New"),("Offer Received","Offer Received"),("Offer Accpeted","Offer Accepted"),("Solde","Solde"),("Cancelled","Cancelled")],copy=False,default="New")
    total_area= fields.Integer(compute = "_compute_total_area")
    best_price=fields.Float(compute="_compute_best_price")



    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self: 
            record.total_area=record.garden_area+record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self: 
            if record.offer_ids:
                record.best_price=max(record.mapped('offer_ids.price'))
            else : record.best_price=0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden==True:
            self.garden_area=10
            self.garden_orientation="North"
        if self.garden==False:
            self.garden_area=0
            self.garden_orientation=None
