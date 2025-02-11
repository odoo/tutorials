from odoo import fields, models, api, exceptions
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate properties"

    name = fields.Char('Title', required=True, translate=True)
    tags_ids = fields.Many2many('estate.property.tag', string='Tags')
    property_type = fields.Many2one('estate.property.type', string='Property Type')
    salesman = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id')  # we have give the Many2one field defined in the comodel in the One2many field, because One2many relationship is virtual, it only exist when corrensponding Many2one field exist in the comodel.
    description = fields.Text('Description')
    postcode = fields.Char('Postcode', required=True)
    date_availability = fields.Date('Available From', copy=False, default=fields.Datetime.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    best_offer = fields.Float('Best Offer', compute="_compute_best_offer")
    bedrooms = fields.Integer('Bedrooms', default="2")
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    total_area = fields.Integer('Total Area (sqm)', compute="_compute_total_amount")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')],
        help="Defines the orientation of the garden")
    active = fields.Boolean('Active', default="True")
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'),
        ('offer received', 'Offer Received'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')],
        help="Status of the Property",
        required=True,
        copy=False,
        default="new")

    @api.depends("living_area", "garden_area")
    def _compute_total_amount(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.mapped('offer_ids.price'), default=0)
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
            # return {'warning': {
            #     'title': ("Warning"),
            #     'message': ('This option is not supported for property types other than House, willa, tenaments')}}
        elif self.garden == False:
            self.garden_area = None
            self.garden_orientation = None
    
    def action_sold_property(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError("Cancelled property can not be sold")
            else:
                record.state = "sold"
        return True
    
    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("Sold property can not be cancel")
            else:
                record.state = "cancelled"
        return True
