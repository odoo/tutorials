from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api,fields,models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Management Module"
    _order= "id desc"

    name = fields.Char('Property Name', required=True)
    description=fields.Text('Description' )
    postcode = fields.Char('Postcode')
    date_availability=fields.Date( 'Available From', copy=False, default= (datetime.today() + relativedelta(months=3)).date())
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection( 
                selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
                string='Garden Orientation') 
    active=fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string='State',
        required=True,
        default='new',  
        copy=False)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", auto_join=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', string='Salesman', index=True, ondelete="cascade")
    partner_id = fields.Many2one('res.partner', string='Buyer', index=True, ondelete="cascade")
    tag_ids=fields.Many2many("estate.property.tag", string="Property Tags", ondelete="cascade" )
    offer_ids = fields.One2many('estate.property.offer','property_id',string='Offers')
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    property_image=fields.Image()
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")


    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation=None
        else:
            self.garden_area=10
            self.garden_orientation='north'
    

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be strictly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price must be non-negative",
        ),
    ]


    @api.depends("garden_area","living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if not record.offer_ids:
                record.best_price=0
                continue
            record.best_price = max(record.offer_ids.mapped('price'))
    

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_cancelled(self):
        for record in self:
            if record.state in ['offer_accepted', 'sold', 'offer_received']:
                raise UserError("Can't delete this Record either property is sold or Offer is received or accepted")


    def action_sell(self):
           for record in self:
            if (
                record.state == "new"
                or record.state == "offer_accepted"
                or record.state == "offer_received"
            ):
                record.state = "sold"
            elif record.state == "cancelled":
                raise UserError("Canceled property can't be sold")
            else:
                raise UserError("Property already sold")


    def action_cancel(self):
          for record in self:
            if (
                record.state == "new"
                or record.state == "offer_accepted"
                or record.state == "offer_received"
            ):
                record.state = "cancelled"
            elif record.state == "sold":
                raise UserError("Sold property can't be canceled")
            else:
                raise UserError("Property already canceled")


    def action_make_offer(self):
        print(self)
        return {
            'name': 'Make Bulk Offer',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'view_mode': 'form',
            'res_model': 'estate.property.make.bulk.offer',
        }
