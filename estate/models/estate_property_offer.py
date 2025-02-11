from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer (models.Model):
    _name = "estate_property_offer_model"
    _description = "hiiii"

    price = fields.Float()
    status = fields.Selection(
        # default="accepted",
        copy=False,
        selection = [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate_model', required=True)
    create_date = fields.Datetime(default=fields.Date.today(), readonly=True)
    validity = fields.Integer('Validity (Days)', default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    ###### compute methods #####
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                deadline = fields.Datetime.from_string(record.create_date) + timedelta(days=record.validity)
                record.date_deadline = deadline.date()

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = fields.Datetime.from_string(record.create_date)
                validity = (fields.Datetime.from_string(record.date_deadline) - create_date).days
                record.validity = validity

    def action_confirm(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("this offer is allready acceplted")

            existing_record = self.search([("property_id", "=", record.property_id.id), ("status", "=", "accepted")], limit=1)
            if existing_record:
                raise UserError("another offer is already accepted")

            record.status = "accepted"
            record.property_id.write({
                'buyer' : record.partner_id.id,
                'selling_price' : record.price
            })
        return True
    
    def action_cancel(self):
        for record in self:
            record.status = "refused"
        return True