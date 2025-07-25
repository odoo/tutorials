from odoo import api, fields, models
from odoo.exceptions import UserError


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
            if record.date_deadline:
                record.validity = (record.date_deadline - create_date).days
            else:
                record.validity = 0

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

        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'
        self.property_id.buyer = self.partner_id

    def action_set_refused(self):
        self.status = 'refused'
