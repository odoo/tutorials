from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline'
    )
    price = fields.Float(
        string='Price',
        required=True
    )

    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string='Status',
        copy=False
    )

    validity = fields.Integer(string="Validity (days)", default=7)

    # Many2one → res.partner (the buyer making the offer)
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        required=True
    )

    # Many2one → estate.property (which property this offer is for)
    # This is the REQUIRED inverse field for the One2many on the property
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.date_deadline = fields.Date.add(date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.validity = (
                    record.date_deadline - date
            ).days

    def action_accept(self):
        for record in self:
            already_accepted = record.property_id.offer_ids.filtered(
                lambda o: o.status == 'accepted' and o.id != record.id
            )
            if already_accepted:
                raise UserError("An offer has already been accepted for this property!")
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("You cannot refuse an already accepted offer!")
            record.status = 'refused'
        return True
