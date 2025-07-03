from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ('price_positive',
         'CHECK(price > 0)',
         'The offer price must be strictly positive.'
         )
    ]

    # misc
    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')],
        copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    # computed
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline',
                                string='Deadline')
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            safe_create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(safe_create_date,
                                                   days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            safe_create_date = record.create_date or fields.Date.today()
            delta = (
                record.date_deadline - fields.Date.to_date(safe_create_date))
            record.validity = delta.days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            new_price = vals.get('price', 0.0)

            if property_id:
                property = self.env['estate.property'].browse(property_id)

                if property.state == 'sold':
                    raise UserError(
                        'The property %s is already sold.' % property.name
                    )

                max_offer = max(property.offer_ids.mapped('price'),
                                default=0.0)
                if new_price < max_offer:
                    raise ValidationError(
                        ('The offer cannot be lower than %.2f.') % max_offer
                    )

                if property.state == 'new':
                    property.state = 'offer_received'

        return super().create(vals_list)

    def action_accept_offer(self):
        for record in self:
            # refuse other offers
            other_offers = self.search([
                ('property_id', '=', record.property_id.id),
                ('id', '!=', record.id)
            ])
            other_offers.write({'status': 'refused'})

            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            record.property_id.state = 'offer_accepted'
            record.status = 'accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
