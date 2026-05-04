from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    _check_price = models.Constraint(
        'CHECK (price > 0.00)',
        'The offer price must be greater than 0 and must be positive',
    )

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
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        store=True
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.date_deadline = fields.Date.add(date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date = (fields.Date.to_date(record.create_date)
                    or fields.Date.today())
            record.validity = (record.date_deadline - date).days

    def action_accept(self):
        self.ensure_one()
        if self.property_id.state in ('sold', 'cancelled'):
            raise ValidationError("Already sold or cancelled property can not accept the offer!")
        (self.property_id.offer_ids - self).write({'status': 'refused'})
        self.write({'status': 'accepted'})
        self.property_id.write({
            'buyer_id': self.partner_id.id,
            'selling_price': self.price,
            'state': 'offer_accepted',
        })
        return True

    def action_refuse(self):
        if self.property_id.state == 'cancelled':
            raise UserError("You cannot reject an offer in a sold or cancelled property")
        if self.status == 'accepted':
            self.property_id.selling_price = 0
            self.property_id.buyer_id = False
            self.property_id.state = 'offer_received'
        self.status = 'refused'
        return True
