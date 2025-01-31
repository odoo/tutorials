from odoo import api,fields, models,exceptions
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
    state = fields.Selection([("New","New"),("Offer Received","Offer Received"),("Offer Accpeted","Offer Accepted"),("Sold","Sold"),("Cancelled","Cancelled")],copy=False,default="New")
    total_area= fields.Integer(compute = "_compute_total_area")
    best_price=fields.Float(compute="_compute_best_price")
    _order="id desc"
    



    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self: 
            record.total_area=record.garden_area+record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self: 
            if record.offer_ids:
                print("TEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEST")
                print("the print before record.mapped")
                print(record.mapped('offer_ids.price'))
                print("the print before record.offer_ids")
                print(record.offer_ids.mapped('price'))
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

    def action_sold(self):
        if self.state=="Cancelled":
            raise exceptions.UserError("impossible car la propriété est cancelled")
        else :
            self.state="Sold"
        return True

    def action_cancelled(self):
        if self.state=="Sold":
            raise exceptions.UserError("impossible car la propriété est sold")
        else :
            for record in self:
                record.state="Cancelled"
        return True

    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price >= 0)',
         'The price hase to be positive'),
         ('selling_price_positiv','CHECK(selling_price >= 0)','the selling price has to be positive')
    ]

    @api.constrains('selling_price','expected_price')
    def _check_selling_price_90(self):
        for record in self: 
            if record.selling_price<0.9*(record.expected_price):
                raise exceptions.ValidationError("the selling prise is lower than 90 pourcent of the expected price")
