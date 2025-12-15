from dateutil.relativedelta import relativedelta
from odoo import fields, models,api,exceptions


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    _positif_expected_price = models.Constraint("CHECK (expected_price > 0)","A price can't be negatif");
    _positif_selling_price = models.Constraint("CHECK (selling_price > 0)","A price can't be negatif");
    _postif_best_price = models.Constraint("CHECK (best_price > 0)", "A price can't be negatif");

    state = fields.Selection(selection = [("New","New"), ("Offer_Received","Offer Received") ,("Offer_Accepted","Offer Accepted"), ("Sold","Sold"), ("Cancelled","Cancelled")])
    active = fields.Boolean('Active',default=True)
    name = fields.Char(required=True,default="Unkown")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From",copy=False,default= fields.Datetime.today() + relativedelta(months=3))
    last_seen= fields.Date("Last Seen", default=fields.Datetime.now)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    best_price = fields.Float(string="Best Price",compute="_get_best_price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('North','North'),('South','South'),('East','East'),('West','West')])
    total_area = fields.Float(compute="_get_total_area",string="Total Area");
    property_type_id = fields.Many2one("estate.property.type",string="Type")
    buyer_id = fields.Many2one("res.partner",string="Buyer")
    seller_id = fields.Many2one("res.users",default=lambda self : self.env.user,string="Seller")
    tag_ids = fields.Many2many("estate.property.tag",string="Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id",string="Offers")

    def sell_property(self):
        for record in self:
            if(record.state == "Cancelled"):
                raise exceptions.UserError("Can't sell cancelled property.")
            record.state = "Sold"
            return True
        
    def cancel_property(self):
        for record in self:
            if(record.state == "Sold"):
                raise exceptions.UserError("Can't cancel sold property.")
            record.state = "Cancelled"
            return True

    @api.depends('living_area','garden_area')
    def _get_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area;


    @api.depends('offer_ids')
    def _get_best_price(self):
        for record in self:
            max:int = 0

            if(len(record.offer_ids)==0):
                record.best_price = 0
                continue
        
            for offer in record.offer_ids:
                if(offer.price >= max):
                    max = offer.price
                record.best_price = max

    @api.onchange("garden")
    def _garden_pre_fill(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'North' if self.garden else ''