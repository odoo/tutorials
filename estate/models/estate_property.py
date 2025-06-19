from odoo import api, fields, models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate properties"

    name = fields.Char("Estate name",required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Date availability",default=fields.Date.today() + relativedelta(months=3),copy=False)
    expected_price = fields.Float("Expected price")
    selling_price = fields.Float("Selling price",readonly=True,copy=False)
    bedrooms = fields.Integer("Number of bedrooms",default=2)
    living_area = fields.Integer("Living area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden area")
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
        help="This Type is used to tell the garden orientation for a property"
    )
    active = fields.Boolean("Active",default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', "New"), ('offer_received', "Offer received"), ('offer_accepted', "Offer Accepted"), ('sold', "Sold"), ('cancelled', "Canceled")],
        help="This is the state of the property",
        default="new",
        required=True,
        copy=False
    )
    property_type_id = fields.Many2one('estate.property.type')
    salesperson_id = fields.Many2one('res.users')
    buyer_id = fields.Many2one('res.partner')
    tag_ids = fields.Many2many('estate.property.tag')
    offers_ids = fields.One2many('estate.property.offer','property_id',string="Offers")

    total_area = fields.Integer(compute='_compute_total')
    best_price = fields.Float(compute='_compute_best_price')

    cancelled = fields.Boolean(default=False)
    sold = fields.Boolean(default=False)


    @api.depends('living_area','garden_area')
    def _compute_total(self):
        self.total_area = self.garden_area + self.living_area

    @api.depends('offers_ids.price')
    def _compute_best_price(self):
        if self.offers_ids.mapped('price'):
            self.best_price = max(self.offers_ids.mapped('price'))
        else:
            self.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sold(self):
        for record in self:
            if not record.state == "cancelled":
                record.state = "sold"
            else:
                raise UserError("You can't sold an house that has been cancelled")
        return True
    
    def action_cancel(self):
        for record in self:
            if not record.state == "sold":
                record.state = "cancelled"
            else:
                raise UserError("You can't cancel an house that has already been sold")
        return True
