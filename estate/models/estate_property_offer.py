from odoo import fields, models, api, _
from datetime import date, timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection([
        ('accepted', "Accepted"),
        ('refused', "Refused")
    ], copy=False)
    property_id = fields.Many2one('estate.property', required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_validity')
    property_type = fields.Many2one(related="property_id.property_type_id", string="Property Type")

    _check_positive_offer = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be positive'
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else date.today()
            record.validity = (record.date_deadline - create_date).days

    def action_accept_offer(self):
        newr = (self.property_id.offer_ids).grouped('partner_id')

        print('newr is: ', newr)

        for record in self.property_id.offer_ids:
            if record.status == 'accepted':
                raise UserError(_('Offer is already accepted'))
        if self.property_id.state in ['sold', 'cancelled']:
            raise UserError(_('The offer cannot be accepted because the property is already sold or cancelled'))

        # method 1:to to refuse all the other offers
        (self.property_id.offer_ids - self).status = 'refused'

        # method 2
        # (self.property_id.offer_ids - self).write({'status': 'refused'})

        # method 3
        # newl = self.property_id.offer_ids.mapped('id')
        # records = self.env['estate.property.offer'].browse(newl) - self
        # records.write({'status': 'refused'})

        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.status = 'accepted'
        self.property_id.state = 'offer accepted'
        return True

    def action_reject_offer(self):
        if self.property_id.state in ['sold', 'cancelled']:
            raise UserError(_('The offer cannot be refused because the property is already sold or cancelled'))
        if self.status == 'accepted':
            self.status = 'refused'
            self.property_id.selling_price = 0
            self.property_id.state = 'new'
            self.property_id.buyer_id = False

        return True
