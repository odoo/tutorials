from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), days=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, default=0.1)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute='_compute_total_area', store=True)
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')]
    )
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    state = fields.Selection(
        string="State",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')],
        default='new',
        required=True,
        copy=False
    )
    active = fields.Boolean(default=False)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_offer = fields.Float(compute="_compute_best_offer", store=True)

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0.0)
    
    def action_sold(self):
        if not self.state == 'canceled':
            self.write({
                'state': 'sold',
            })
            return True
        else:
            raise UserError("The property has been canceled")
        
    def action_cancel(self):
        if not self.state == 'sold':
            self.write({
                'state': 'canceled',
            })
            return True
        else:
            raise UserError("The property has been sold")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_correct_states(self):
        state_description_values = {elem[0]: elem[1] for elem in self._fields['state']._description_selection(self.env)}
        for property in self.filtered(lambda property: property.state not in ['new', 'canceled']):
            raise UserError(_('You cannot delete a property which is in %s state.', state_description_values.get(property.state)))
        return True

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be strictly positive'),
    ]
