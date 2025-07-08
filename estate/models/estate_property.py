from odoo import  fields,models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property is defined"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_avaiblity = fields.Date(copy = False, default = date.today()+ relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Direction',
        selection=[('north','North'), ('south','South'), ('east','East'), ('west','West')],
        help = "This is used to locate garden's direction"
    )
    active = fields.Boolean(default = True)
    state = fields.Selection(
        selection=[('new','New'), ('offer received','Offer Received'), ('offer accepted','Offer Accepted'), ('sold','Sold'), ('cancelled', 'Cancelled')],
        default = 'new',
        required = True,
        copy = False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one('res.users', string='Salesman', index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one(
    'res.partner', 
    string='Buyer', 
    index=True, 
    tracking=True,  
    default=lambda self: self.env.user.partner_id.id
)
    _sql_constraints = [
        ('check_expectep_price', 'CHECK(expected_price > 0 AND selling_price > 0)',
         'The Price must be positve.')
    ]
    
    property_tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(compute="_compute_total")

    @api.depends("garden_area","living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    best_price = fields.Float(compute="_compute_best_price", string="Best Offer Price" ,readonly = True)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            record.state = 'cancelled'

    # SOLD button logic
    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be marked as sold.")
            record.state = 'sold'

    _order = "id desc"

    