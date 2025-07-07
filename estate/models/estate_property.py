from dateutil.relativedelta import relativedelta
from odoo import models,fields,api,_
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(required=True,string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
    default=lambda self: fields.Date.today() + relativedelta(months=3),
    copy=False,string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    total_area = fields.Float(compute='_compute_total_area',store=True)
    facades = fields.Integer()
    garage  = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West')
    ],string="Garden Orientation")
    state = fields.Selection(
    [
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ],
    required=True,
    copy=False,
    default='new')
    property_type_id = fields.Many2one(
        "estate.property.types", string="Property Type"
    )
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", copy=False
    )
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many('estate.property.tags',string="Tags")

    offer_ids = fields.One2many('estate.property.offer','property_id',string="Offers")

    best_price = fields.Float(compute='_get_best_offer_price',store=True)



    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    @api.depends('offer_ids.price')
    def _get_best_offer_price(self):
        for record in self:
            prices=record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = ''

    def action_set_state_sold(self):
        for record in self:
            if(record.state == 'cancelled'):
                raise UserError(_("Cancelled property cannot be sold."))
                print("Cancelled can't be sold")
            else:
                record.state = 'sold'
        return True

    def action_set_state_cancel(self):
        for record in self:
            if(record.state == 'sold'):
                raise UserError(_("Sold property cannot be cancelled."))
                print("Sold can't be cancelled")
            else:
                record.state = 'cancelled'
        return True