from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate property details"
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive!'),
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive!'),
        ('unique_property_name', 'UNIQUE(name)', 'The property name must be unique!')
    ]
    
    name = fields.Char(required=True, string="Property Name", tracking=True)
    description = fields.Text(string="Descriiption",tracking=True)
    postcode = fields.Char(string="postcode", tracking=True)
    image_1920 = fields.Image("Property Image", max_width=1920, help="Upload an image of the property")
    date_availability = fields.Date(copy=False,tracking=True)
    expected_price = fields.Float(string="Expected Price",required=True,tracking=True)
    selling_price = fields.Float(string="Selling Price",copy=False,tracking=True)
    bedrooms = fields.Integer(string="Bedrooms",default=2,tracking=True)
    living_area = fields.Integer(string="Living Area (sq m)")
    facades = fields.Integer(string="Facades")
    active = fields.Boolean(default=True)
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden",default=True)
    garden_area = fields.Integer(string="Garden AreG")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
           ('north', "North"),
           ('south', "South"),
           ('west', "West"),
           ('east', "East")
        ]
    )
    state = fields.Selection(
        string="Property State",
        required=True,
        store=True,
        copy=False,
        default='new',
        tracking=True,
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ]
    ) 
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    offer_ids = fields.One2many('estate.property.offer','property_id', string="Property Offer")
    salesperson_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", readonly=True)
    company_id = fields.Many2one(
        'res.company', 
        string="Company Name", 
        required=True, 
        default=lambda self: self.env.user.company_id
    )
    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True)
    invoice_count = fields.Integer(string="Invoices", compute='_compute_invoice_count')
    total_area = fields.Float(string="Total Area (sq.m)", compute='_compute_total_area', store=True)
    best_offer = fields.Float(string="Best Offer", compute='_compute_best_offer', store=True)
  
    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
    
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0.0)
    
    @api.depends('buyer_id')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = self.env['account.move'].search_count([
                ('partner_id', '=', record.buyer_id.id),
                ('move_type', '=', 'out_invoice'),
                ('property_id', '=', record.id)
            ]) if record.buyer_id else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False

    @api.constrains('selling_price')
    def _check_selling_price(self):
            if any(record.selling_price and record.selling_price < record.expected_price * 0.9 for record in self):
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _ondelete_check_state(self):
            if any(record.state not in ('new', 'cancelled') for record in self):
                raise UserError("You cannot delete a property that is not in 'New' or 'Cancelled' state.")
    
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state='cancelled'

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Canceled properties cannot be sold.")
            if not record.selling_price:
                raise UserError("Selling price is not set. Please set a selling price before marking as sold.")
            if not record.buyer_id:
                raise UserError("Buyer is not set. Please assign a buyer before marking as sold.")
            accepted_offer = record.offer_ids.filtered(lambda offer: offer.status == 'accepted')
            if not accepted_offer:  # No accepted offer found
                raise UserError("You cannot sell a property without an accepted offer.")
            record.state = 'sold'

    def action_view_invoice(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([
            ('partner_id', '=', self.buyer_id.id),
            ('move_type', '=', 'out_invoice')
        ])
        if not invoices:
            raise UserError("No invoices found for this property.")
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        return action
