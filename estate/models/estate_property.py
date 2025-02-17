from datetime import timedelta
from odoo import _, api, exceptions, fields, models


class EstateProperty(models.Model):
    _name="estate.property"
    _description="Estate Property"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available from", copy=False, default = fields.Date.today() + timedelta(days=+90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection([
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
        ], string='Direction',)
    active = fields.Boolean(default=True)
    state = fields.Selection([
            ('new','New'),
            ('offer recieved','Offer Recieved'),
            ('offer accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled'),
        ], string="Status", default='new', required=True, copy=False)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Seller", index=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", string="Total area")
    best_price = fields.Float(compute="_compute_best_price", string="Best price")
    estate_property_seq = fields.Char(string="Estate Property Sequence", readonly=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_price', 'CHECK(expected_price > 0.0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0.0)', 'The Selling price must be strictly positive'),
    ]
    
    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            offer_ids = record.offer_ids
            if offer_ids:
                record.best_price = max(offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        if self.selling_price and self.selling_price < self.expected_price *0.9:
            raise exceptions.ValidationError("Selling price cannot be lower than 90% of the expected price")

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            if not vals.get('estate_property_seq'):
                vals['estate_property_seq'] = self.env['ir.sequence'].next_by_code('estate.property.seq')
        return super().create(vals_list) 

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("Cancelled property cannot be sold")
            if record.state == 'offer accepted':
                record.state = 'sold'
            else:
                raise exceptions.UserError("Offer must be accepted")

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Sold property cannot be cancelled")
            else:
                record.state = 'cancelled'

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise exceptions.UserError("Only New and Cancelled properties can be deleted")
