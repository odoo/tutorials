from odoo import models, fields, api
from datetime import date
from datetime import timedelta
from odoo.exceptions import UserError


class estate_property_offer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property offer"
    price = fields.Float()
    _order = "sequence, price desc"
    sequence = fields.Integer('Sequence')
    _sql_constraints = [
        ('offer_price', 'CHECK(price > 0)', 'offer price must be strictly positive')
    ]
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_validity", string="Deadline")
    property_type_id = fields.Many2one(related="property_id.property_type", store=True)

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            today = record.create_date
            if today:
                today = record.create_date
            else:
                today = date.today()
            if record.date_deadline:
                record.date_deadline = today + (record.validity - (record.date_deadline - today).days)
            else:
                record.date_deadline = timedelta(days=record.validity) + today

    @api.ondelete(at_uninstall=False)
    def _deletion_check(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.buyer_id = None
                record.property_id.selling_price = 0

    def _inverse_validity(self):
        for record in self:
            today1 = fields.Date.from_string(record.create_date)
            updated_deadline_date = fields.Date.from_string(record.date_deadline)
            record.validity = (updated_deadline_date - today1).days

    def action_confirm(self):
        if self.property_id.buyer_id:
            raise UserError("Validation Error!, It is already accepted")
        else:
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.status = 'accepted'
            self.property_id.state = 'offer_accepted'

    def action_refused(self):
        if self.status == 'accepted' and self.property_id.buyer_id == self.partner_id:
            self.status = 'refused'
            self.property_id.buyer_id = None
            self.property_id.selling_price = 0
            self.property_id.state = 'new'
        else:
            self.status = "refused"
