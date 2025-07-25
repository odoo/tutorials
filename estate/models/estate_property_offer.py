from odoo import exceptions, api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('DeadLine', compute='_compute_deadline', inverse='_inverse_deadline')

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price should be strictly positive')]

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            base_date = (record.create_date or fields.Datetime.now()).date()
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            base_date = (record.create_date or fields.Datetime.now()).date()
            record.validity = (record.date_deadline - base_date).days

    def action_set_accepted(self):
        for record in self:
            property_rec = record.property_id

            if property_rec.status in ('sold', 'cancelled'):
                raise exceptions.UserError("You cannot accept an offer on a sold or cancelled property.")

            # prevent more than one accepted offer
            already_accepted = property_rec.offer_ids.filtered(lambda ele: ele.status == 'accepted')
            if already_accepted and record not in already_accepted:
                raise exceptions.UserError("Only one offer can be accepted for a property.")

            record.status = 'accepted'

            # set buyer & selling price on the property
            property_rec.write({
                'partner_id': record.partner_id,
                'selling_price': record.price,
                'status': 'offer_accepted',
            })
        return True

    def action_set_rejected(self):
        for record in self:
            record.status = 'refused'
