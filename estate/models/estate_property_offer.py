from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "id"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity (days)")
    deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.deadline - fields.Date.today()).days

    def action_accept(self):
        if 'accepted' in self.mapped("property_id.offer_ids.status"):
            raise UserError("An offer is already accepted")
        else:
            for record in self:
                record.status = 'accepted'
                record.property_id.state = 'offer_accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
