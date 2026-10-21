from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"

    property_id = fields.Many2one('estate.property', string='Property')

    price = fields.Float(string='Price', required=True)
    buyer_id = fields.Many2one('res.partner', string='Partner', index=True)
    state = fields.Selection(
        [('refused', 'Refused'),
         ('accepted', 'Accepted'),
         ('waiting', 'Waiting')],
        default='waiting'
    )

    _check_price_strict_positive = models.Constraint(
        'check(price > 0)',
        'Expected price must be strictly positive.',
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Datetime(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Date.add(offer.create_date, days=offer.validity)
            else:
                offer.date_deadline = fields.Date.add(fields.Date.today(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline.date() - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            record.state = 'accepted'
            record.property_id._accept_offer(record)
        return True

    def action_refuse(self):
        for record in self:
            record.state = 'refused'
        return True
