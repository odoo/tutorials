from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import float_utils


class estate_Properties(models.Model):
    _name = "estate.properties"
    _description = "Information of Properties"
    _order = "id desc"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    Postcode = fields.Char("PostCode")
    date_avaibility = fields.Date(string = "Available From", copy = False, default = fields.Date.today() + relativedelta(months=+3))
    expected_price = fields.Float(string = "Expected Price")
    selling_price = fields.Float(copy=False)
    Bedrooms = fields.Integer()
    living_area = fields.Integer(string = "Living Area (sqm)")
    facades = fields.Integer("Is Facades Available")
    garage = fields.Boolean("Is Garage Available")
    garden = fields.Boolean("Is Garden Available")
    garden_area = fields.Integer(string = "Garden Area (sqm)")
    garden_orientation = fields.Selection([('north','North'),('south' , 'South'),('east','East'),('west','West')],string = "Garden Orientation")
    active = fields.Boolean('Active', default=True)
    status = fields.Selection([('new','New'),('offer recieved' , 'Offer Recieved'),('offer accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')], default="new")
    property_ids = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one("res.partner", copy=False)
    sales_person_ids = fields.Many2one("res.users", string="Salesman", default = lambda self: self.env.user)
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many('estate.property.offer','property_id', string='Properties')
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total")
    best_offer = fields.Float("Best Offer", compute="_compute_best_offer")

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0)','The expected price must be strictly positive.'),
        ('selling_price', 'CHECK(selling_price >= 0)','The selling price must be strictly positive.')
    ]



    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area 

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:   
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("best_offer")
    def _onchange_best_offer(self):
        if self.best_offer > 0:
            self.status="offer recieved"

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold(self):
        if self.status == 'cancelled':
            raise UserError("A cancelled property cannot be sold.")
        else:
            for record in self.offer_ids:
                if record.status == "accepted": 
                    self.status = "sold" 
                    break
            if self.status != "sold":
                raise UserError("Accept an offer first.")                             

    def action_cancelled(self):
        for record in self:
            if record.status == 'sold':
                raise UserError("A sold property cannot be cancelled.")
            record.status = 'cancelled'

    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
            if self.selling_price != 0:
                if float_utils.float_compare(self.selling_price,0.9*self.expected_price,precision_digits=2)<=0:
                    raise UserError("selling price must be grater than 90 percent of the expected price")
