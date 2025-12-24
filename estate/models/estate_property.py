from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"
    _order = 'id desc'

    name = fields.Char("Title", required=True, translate=True)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type",
    )
    postcode = fields.Char("Postcode", required=True)
    availability = fields.Date(
        "Available From",
        required=True,
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    description = fields.Text("Description")
    bedrooms = fields.Integer("Bedrooms", required=True, default=2)
    living_area = fields.Integer("Living Area (sqm)", required=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id.id)
    expected_price = fields.Monetary("Expected Price", required=True)
    selling_price = fields.Monetary("Selling Price", readonly=True, copy=False)
    # best_offer_id = fields.Many2one('estate.property.offer', string='Best Offer', readonly=True)
    facades = fields.Integer("Facades", default=False)
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Garden", default=False)
    garden_area = fields.Integer("Garden Area (sqm)", required=False)
    garden_orientation = fields.Selection(selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")], string="Garden Orientation")
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    total_area = fields.Integer("Total Area (sqm)", compute='_compute_area')
    @api.depends('garden_area', 'living_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    state = fields.Selection(
        string="Status",
        selection=[('new', "New"), ('offer_received', "Offer Received"), ('offer_accepted', "Offer Accepted"), ('sold', "Sold"), ('canceled', "Canceled")],
        required=True,
        copy=False,
        default='new',
    )
    def sold_action(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise UserError(record.env._("You can not sell a canceled property."))
        return True
    def cancel_action(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise UserError(record.env._("You can not cancel a sold property."))
        return True
    active = fields.Boolean("Active", default=True)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    seller_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string="Tags",
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string="Offers",
    )
    best_offer = fields.Monetary(
        string="Best Offer",
        compute='_compute_best_offer',
    )
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.0

    def write(self, vals):
        result = super().write(vals)
        if 'offer_ids' in vals:
            for record in self:
                if record.offer_ids and record.state == 'new':
                    record.state = 'offer_received'
                elif not record.offer_ids and record.state == 'offer_received':
                    record.state = 'new'
        return result

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        "The expected price should be higher than zero.",
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        "The selling price can't be negative",
    )
    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        if any((not(record.state == 'new') and not(record.state == 'canceled'))
        for record in self):
            raise UserError("Only new and canceled properties can be deleted!")
