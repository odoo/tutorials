from datetime import date, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Property(models.Model):
    _name = 'estate.property'
    _description = "Test description for estate.property model"
    _order = 'id DESC'

    name = fields.Char(required=True)
    expected_price = fields.Float(required=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    state = fields.Selection(
        selection=[('new', "New"), ('offer_received', "Offer Received"), ('offer_accepted', "Offer accepted"), ('sold', "Sold"), ('cancelled', "Cancelled")],
        default='new',
    )
    description = fields.Text()
    postcode = fields.Char()
    selling_price = fields.Float(copy=False, readonly=True)
    date_availability = fields.Date(copy=False, default=lambda _: date.today() + timedelta(days=90))
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")])
    active = fields.Boolean(default=True)
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesperson_id = fields.Many2one('res.users', string="Salesperson", copy=False, default=lambda self: self.env.user)
    tags_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Float(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        "The expected price must be strictly positive",
    )
    _check_selling_price = models.Constraint(
        'CHECK (selling_price >= 0)',
        "The selling price must be positive",
    )

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(o.price for o in record.offer_ids) if record.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_prevent_deletion_unless_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(_("A property can only be deleted if its state is 'New' or 'Cancelled'"))

    def action_property_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("A sold property cannot be cancelled."))
            record.state = 'cancelled'
        return True

    def action_property_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_("A cancelled property cannot be sold."))
            record.state = 'sold'
        return True
