from odoo import api, fields, models


class AwesomeEstatePropertyOffer(models.Model):
    _name = 'awesome.estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc, id desc'

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        required=True,
    )
    property_id = fields.Many2one(
        'awesome.estate.property',
        string="Property",
        required=True,
        ondelete='cascade',
        index=True,
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    fields.Date.to_date(record.create_date), days=record.validity,
                )
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity,
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = fields.Date.to_date(record.date_deadline) - fields.Date.to_date(record.create_date)
                record.validity = delta.days
            elif record.date_deadline:
                delta = fields.Date.to_date(record.date_deadline) - fields.Date.today()
                record.validity = delta.days if delta.days > 0 else 0
