from odoo import api, fields, models


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

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            date = (
                record.create_date.date()
                if record.create_date
                else fields.Date.today()
            )
        record.date_deadline = fields.Date.add(date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date = (
                record.create_date.date()
                if record.create_date
                else fields.Date.today()
            )
            record.validity = (
                    record.date_deadline - date
            ).days

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
