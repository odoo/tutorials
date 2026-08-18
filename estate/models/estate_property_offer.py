from odoo import exceptions, api, fields, models
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate offer model"

    name = fields.Char(required=True)
    price = fields.Float()
    status = fields.Selection(
            string='status',
            copy=False,
            selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
        )
    partner_id = fields.Many2one("res.users", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    date_deadline = fields.Datetime(string="Deadline", compute="compute_deadline", inverse="_inverse_deadline")
    validity = fields.Integer(string="validity", default=7)

    @api.depends('validity', "create_date")
    def compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Datetime.today() + relativedelta(days=record.validity)
                
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    #===========button actions===========
    def action_accept(self):

        for record in self:
            if "accepted" in record.property_id.offer_ids.mapped("status"):
                raise exceptions.UserError("already accepted an offer!")
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.status = "accepted"

    def action_refuse(self):
        for record in self:
            for property in record.property_id:
                record.status = "refused"
