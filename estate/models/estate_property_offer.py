from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperties(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offers'
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date(compute='_compute_deadline',
                                inverse="_inverse_deadline", string="Deadline", store=True)
    property_type_id = fields.Many2one(
        'estate.property.types',
        related='property_id.property_type_id',
        store=True,
    )

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The offer price must be positive'),
    ]

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date.date(
            ) if record.create_date else fields.Date.context_today(record)
            record.date_deadline = fields.Date.add(
                create_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days if record.date_deadline else 0

    def action_set_accepted(self):
        for offer in self:
            accepted_offer = self.search([
                ('property_id', '=', offer.property_id.id),
                ('status', '=', 'accepted'),
                ('id', '!=', offer.id)
            ], limit=1)

            if accepted_offer:
                raise UserError(
                    "Already accepted other offer!!")

            offer.status = 'accepted'
            other_offers = offer.property_id.offer_ids - offer
            other_offers.write({'status': 'refused'})
            offer.property_id.write({
                'selling_price': offer.price,
                'state': 'offer_accepted',
                'buyer': offer.partner_id.id,
            })

    def action_set_refused(self):
        self.status = 'refused'

    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            property_id = record.get('property_id')
            new_price = record.get('price', 0)

            property_record = self.env['estate.property'].browse(property_id)

            if property_record.offer_ids and any(offer.price > new_price for offer in property_record.offer_ids):
                raise ValidationError("A higher offer already there so can't create an offer!")

            property_record.write({'state': 'offer_received'})

        return super().create(vals)
