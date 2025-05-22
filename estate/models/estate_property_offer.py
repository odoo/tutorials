from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.date_utils import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float()
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    date_deadline = fields.Date('Deadline')
    validity = fields.Integer('Validity (days)', default=7, compute='_compute_validity', inverse='_inverse_validity')
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    property_state = fields.Selection('Property State', related='property_id.state')
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [('check_price', 'CHECK(price > 0)', _('The price must be strictly positive.'))]

    @api.depends('date_deadline')
    def _compute_validity(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.date.today()).days

    def _inverse_validity(self):
        for record in self:
            if isinstance(record.validity, int):
                record.date_deadline = fields.date.today() + relativedelta(days=record.validity)

    def action_accept(self):
        if self.property_id.state in ['offer_accepted', 'sold'] and self.status != 'accepted':
            raise UserError(_('Another offer has already been accepted.'))
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'
        for offer in self.property_id.offer_ids:
            offer.status = 'refused'
        self.status = 'accepted'

    def action_refuse(self):
        if self.status == 'accepted':
            if self.property_id.state == 'sold':
                raise UserError(_('The property has already been sold.'))
            self.property_id.buyer_id = None
            self.property_id.selling_price = None
            self.property_id.state = 'offer_received'
        self.status = 'refused'
