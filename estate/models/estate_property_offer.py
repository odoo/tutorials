from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class estate_property_offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'property offer'
    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price >= 0)', 'An offer price must be strictly positive'),
    ]
    _order = 'price desc'

    price = fields.Float(string = 'price')
    status = fields.Selection([('accepted', 'Accepted'),('refused', 'Refused')], string = 'status')
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default = 7, string = "Validity (days)")
    date_deadline = fields.Date(string = "Deadline", compute = '_compute_date_deadline', inverse='_inverse_date_deadline',  store = True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type", store=True)
    creation_date = fields.Date(default=fields.Date.today(), readonly = True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer.creation_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                delta = offer.date_deadline - fields.Date.today()
                offer.validity = delta.days

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state in ('canceled', 'sold'):
                raise UserError(_("Cannot make changes on a canceled or sold property"))
            offer.property_id.write({
                'selling_price': offer.price,
                'buyer': offer.partner_id,
                'state': 'offer_accepted',
            })
            offer.status = 'accepted'

    def action_refuse_offer(self):
        for offer in self:
            if offer.property_id.state in ('canceled', 'sold'):
                raise UserError(_("Cannot make changes on a canceled or sold property"))
            offer.status = 'refused'
    
    @api.model_create_multi
    def create(self, vals_list):
        for offer in vals_list:
            property = self.env['estate.property'].browse(offer.get('property_id'))
            higher_offer = max(property.offer_ids.mapped('price'), default=0)
            if higher_offer > offer.get('price', 0):
                raise ValidationError(_("Cannot create an offer with a lower price than an existing one"))
        return super().create(vals_list)