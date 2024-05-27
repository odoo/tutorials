from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "estate property offers"

    # simple fields
    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', "Accepted"),
                   ('refused', "Refused"),
                   ],
        copy=False,
        )
    validity = fields.Integer("Validity (Days)", default=7)

    # relational fields
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    # computed fields
    date_deadline = fields.Date("Deadline Date", compute='_compute_deadline', inverse='_inverse_deadline')

    # sql constraints
    _sql_constraints = [
        ('check_positive_offer_price', 'CHECK(price > 0)',
         'The offer price should be strictly positive number.'),
    ]

    # compute methods
    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity) if record.create_date \
            else fields.Date.add(fields.Datetime.today(), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    # action methods
    def action_offer_accept(self):
        for record in self:
            if record.property_id.state in ('sold', 'canceled'):
                raise UserError("Can't modify offers for Sold/Canceled properties")
            elif self._is_any_offer_accepted():
                raise UserError("Another offer was accepted, Refuse it first")
            else:
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.status = 'accepted'
        return True

    def action_offer_refuse(self):
        for record in self:
            if record.property_id.state in ('sold', 'canceled'):
                raise UserError("Can't modify offers for Sold/Canceled properties")
            else:
                record.status = 'refused'
        return True

    # helper funtions
    def _is_any_offer_accepted(self):
        for record in self:
            for p_offer in record.property_id.offer_ids:
                if p_offer.status == 'accepted':
                    return True
        return False
