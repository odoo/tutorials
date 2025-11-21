from odoo import api, models, fields
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "test description"
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='inverse_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    @api.depends('validity')
    def _compute_deadline(self):
        for records in self:
            records.date_deadline = fields.Datetime.add(fields.Date.today(), days=records.validity)

    def inverse_deadline(self):
        for records in self:
            records.validity = (records.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            if not record.property_id.buyer_id:
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
            else:
                raise UserError('An offer has already been accepted')
        return True

    def action_decline(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError('This offer has already been accepted')
            else:
                record.status = 'refused'
        return True

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive'
    )

    @api.model
    def create(self, vals):
        for val in vals:
            property_id = self.env['estate.property'].browse(val['property_id'])
            if property_id.state == "sold":
                raise UserError("You can't create an offer for a sold property")

            for offer in property_id.offer_ids:
                if offer.price > val['price']:
                    raise UserError("You can't create a lower offer than the highest one")
        offers = super().create(vals)
        offers.property_id.state = 'offerreceived'

        return offers
