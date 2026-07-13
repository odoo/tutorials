from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ('Accepted', "Accepted"),
            ('Refused', "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity date", default=7)
    date_deadline = fields.Date(
        string="Deadline date", compute="_compute_date_deadline"
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            #            breakpoint()
            base = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = base + timedelta(record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = record.create_date + timedelta(record.date_deadline)

    def action_accept(self):
        if 'Accepted' in self.property_id.offer_ids.mapped('status'):
            raise UserError("An offer has already been accepted for this property")
        self.status = 'Accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        (self.property_id.offer_ids - self).write({'status': 'Refused'})

    def action_refuse(self):
        self.status = 'Refused'
