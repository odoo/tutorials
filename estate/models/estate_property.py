from dateutil.relativedelta import relativedelta

from odoo import _,api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        string="Availability Date",
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    _check_expected_price = models.Constraint(
        'CHECK( expected_price >=0 )',
        'expected price cannot be less than 0 or in negative value '
    )
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    _check_selling_price = models.Constraint(
        'CHECK( selling_price >= 0 )',
        'selling price cannot be lestt than 0 or in negative value '
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if (
                record.selling_price < 0.90 * record.expected_price
            ):
                raise ValidationError("selling price cannot be less than 90% of expected price")

    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garage_area = fields.Integer(string="Garage Area")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    active = fields.Boolean(default=True, string="Active")
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")

    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default='new',
        string="State",
    )
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string="Garden Orientation",
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", default=lambda self: self.env.user, string="Salesperson"
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Integer(
        string="Best price", compute="_compute_best_price", store="True"
    )
    maintenance_ids = fields.One2many(
        "estate.property.maintenance", 'property_id', string="maintenance_id"
    )

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            price = record.offer_ids.mapped('price')
            record.best_price = max(price) if price else 0.0

    @api.onchange('garden')
    def _on_change_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.onchange('garage')
    def _on_change_garage(self):
        if self.garage:
            self.garage_area = 10
        else:
            self.garage_area = 0

    @api.depends('living_area', 'garden_area', 'garage_area')
    def _compute_total_area(self):
        # breakpoint()
        for record in self:
            record.total_area = (
                record.living_area + record.garden_area + record.garage_area
            )

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("sold property cannot be cancelled ")
            record.state = "cancelled"
        return True

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_("cancelled property cannot be sold"))
            record.state = "sold"
        return True

    def action_accept_best_price(self):
        # for record in self:
        #     best_offer = record.offer_ids.filtered(
        #         lambda o: o.price == record.best_price
        #     )
        #     record.selling_price = record.best_price
        #     record.state = 'sold'
        #     record.buyer_id = best_offer.partner_id
        #     best_offer.status = 'Accepted'
        #     (record.offer_ids - best_offer).write({'status': 'Refused'})

        best_offer = self.offer_ids.filtered(lambda o: o.price == self.best_price)
        self.selling_price = self.best_price
        self.state = 'sold'
        self.buyer_id = best_offer.partner_id
        best_offer.status = 'Accepted'
        (self.offer_ids - best_offer).write({'status': 'Refused'})
        return {
            'effect': {
                'fadeout': 'slow',
                'message': "nice job",
                'image_url': '...',
                'type': 'rainbow_man',
            }
        }
