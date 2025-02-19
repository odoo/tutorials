from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "this is the estate property offer model"
    _sql_constraints = [
        (
            'check_positive_amounts',
            'CHECK (price > 0)',
            'This amount must be positive',
        ),
    ]
    _order = 'price desc'

    price = fields.Float(digits=(20,2))
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False, readonly=True
    )
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True, string='Property Type')
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for property_offer in self:
            if property_offer.create_date:
                create_date = property_offer.create_date.date()
            else:
                create_date = fields.Date.today()
            property_offer.date_deadline = create_date + relativedelta(days=property_offer.validity)

    @api.onchange('date_deadline')
    def _inverse_date_deadline(self):
        for property_offer in self:
            if property_offer.create_date:
                create_date = property_offer.create_date.date()
            else:
                create_date = fields.Date.today()
            property_offer.validity = (property_offer.date_deadline - create_date).days

    def action_accept(self):
        for property_offer in self:
            property_offer.status = 'accepted'
            property_offer.property_id.selling_price = property_offer.price
            property_offer.property_id.buyer_id = property_offer.partner_id
            property_offer.property_id.state = 'accepted'
        return True

    def action_refuse(self):
        for property_offer in self:
            property_offer.status = 'refused'
        return True

    # TODO: should maybe modify vals_list variable and then call super().create
    @api.model_create_multi
    def create(self, vals_list):
        property_offers = super().create(vals_list)
        for property_offer in property_offers:
            if float_compare(property_offer.price, property_offer.property_id.best_price, precision_digits=10) < 0:
                raise UserError("Creating an offer which is worse than another is not allowed")
            property_offer.property_id.state = 'received'
        return property_offers
