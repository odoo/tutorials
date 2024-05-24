from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import add


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    _sql_constraints = [
        ('check_positive_price', 'CHECK (price > 0)', 'The price of an offer should be strictly positive')
    ]

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],
    )

    partner_id = fields.Many2one(
        'res.partner',
        required=True,
    )
    property_id = fields.Many2one(
        'estate.property',
        required=True,
    )

    validity = fields.Integer(
        default='7',
        string='Validity (days)',
        help='Number of days the offer is valid'
    )
    date_deadline = fields.Date(
        compute='_compute_deadline',
        inverse='_inverse_deadline'
    )
    property_type_id = fields.Many2one(
        related='property_id.type_id',
        store=True
    )

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.to_date(add(create_date, days=record.validity))

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = int((record.date_deadline - fields.Date.to_date(record.create_date)).days)

    def action_validate(self):
        self.property_id.offer_ids.update({'status': 'refused'})
        self.property_id.update({'selling_price': self.price, 'buyer': self.partner_id.id, 'state': 'offer_accepted'})
        self.update({'status': 'accepted'})

    def action_cancel(self):
        self.update({'status': 'refused'})

    @api.model
    def create(self, vals):
        if self.env['estate.property.offer'].search_count([
            ('property_id', '=', vals['property_id']),
            ('price', '>', vals['price'])
        ]):
            raise UserError("You're trying to create an offer with a lower price than an existing offer")

        self.env['estate.property'].browse([vals['property_id']]).state = 'offer_received'

        return super().create(vals)
