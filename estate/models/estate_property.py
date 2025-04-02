from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Real estate property model'
    _order = 'sequence, id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(),days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north','North'),('south','South'),('east','East'),('west','West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State of Property',
        selection=[('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson')
    tags_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price', copy=False)
    sequence = fields.Integer('Sequence', default=1)
    image = fields.Image(string='Image')

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price >= 0)', 'Expected price must be strictly positive'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive'),
    ]

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Canceled properties can not be sold.')
            elif 'accepted' not in record.offer_ids.mapped('status'):
                raise UserError('No offer is accepted.')
            else:
                record.state = 'sold'
        return True

    def action_set_cancel(self):
        if self.state == 'sold':
            raise UserError('Sold properties can not be canceled.')
        else:
            self.state = 'canceled'
        return True

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.9:
                raise ValidationError("The selling price must be greater than 90% of expected price!")

    @api.ondelete(at_uninstall=True)
    def _unlink_check_property_state(self):
        for record in self:
            if record.state not in ['new','canceled']:
                raise ValidationError("Only new and canceled properties can be sold!")
