from odoo import fields, models, api, _
from odoo.exceptions import UserError


class EstateModel(models.Model):
    _name = 'estate.property'
    _description = 'Estate properties'

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text()
    postcode = fields.Integer(help='Your post code in 4 or 5 digits.')
    date_availability = fields.Date('Available From', copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (m²)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (m²)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('west', 'West'), ('south', 'South'), ('east', 'East')],
        help='The selection of the garden orientation.')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default='new',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_offer = fields.Float(compute="_find_best_offer")

    @api.depends("offer_ids")
    def _find_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(self.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.0

    @api.onchange("garden")
    def _onchange_has_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
            return {'warning': {
                'title': _("Warning"),
                'message': ('Unchecking the garden option removed the area value and orientation.')}}

    def action_btn_sold(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = "sold"
            else:
                raise UserError("This property is already cancelled and thus cannot be sold anymore.")
        return True

    def action_btn_cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = "cancelled"
            else:
                raise UserError("This property is already sold and thus cannot be cancelled anymore.")
        return True
