from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate properties"
    _order = "id desc"

    name = fields.Char("Name", required=True)
    description = fields.Text("Description", )
    
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    
    facades = fields.Integer("Facades")
    
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")

    image = fields.Image("Image")

    garden_area = fields.Integer("Garden Area")
    
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help = "The garden orientation is used to describe Garden's orientation, lol?"
    )

    total_area = fields.Integer("Total Area", readonly=True, compute="_compute_total_area", store=True)
    active = fields.Boolean("Active", default=True)

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new",
        string="Status",
        required=True,
        readonly=True
    )

    seller_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)

    property_type_id = fields.Many2one("estate.property.type", string="Type", ondelete='cascade')
    property_tags_id = fields.Many2many("estate.property.tag", string="Tags", ondelete='cascade')

    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id")

    best_price = fields.Float("Best Offer", readonly=True, compute="_compute_best_price", store=True)

    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    def action_mark_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('A Cancelled Property Cannot Be Sold')
            else:
                record.state = 'sold'

    def action_mark_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('A Sold Property Cannot Be Cancelled')
            else:
                record.state = 'cancelled'

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("The selling price is lower than the 90% of expected price.")

    @api.ondelete(at_uninstall=False)
    def on_delete(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError('Cannot delete the property which is not in either "New" or "Cancelled" state.')

    def action_make_offer(self):
        return {
            'name': ('Make Offer'),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'view_mode': 'form',
            'res_model': 'estate.property.make.offer',
        }

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price should be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price should be strictly positive.')
    ]
