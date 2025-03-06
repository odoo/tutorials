from odoo import fields, models, api # type: ignore
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class estate_Properties(models.Model):
    _name = "estate.properties"
    _description = "Information of Properties"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    Postcode = fields.Char("PostCode")
    date_avaibility = fields.Date(string = "Available From", copy = False, default = fields.Date.today() + relativedelta(months=+3))
    expected_price = fields.Float(string = "Expected Price")
    Selling_price = fields.Float(readonly=True,copy=False)
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

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area 

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:   
            price1 = record.offer_ids.mapped('price')
            if len(price1)>0:
                record.best_offer = max(record.offer_id.mapped('price'))
            else:
                record.best_offer = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold(self):
        for record in self:
            if record.status == 'cancelled':
                raise UserError("A cancelled property cannot be sold.")
            record.status = 'sold'

    def action_cancelled(self):
        for record in self:
            if record.status == 'sold':
                raise UserError("A sold property cannot be cancelled.")
            record.status = 'cancelled'
