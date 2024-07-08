from odoo import fields, api, models
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offerf"

    partner_id = fields.Many2one('res.partner', string='buyer')
    status = fields.Selection(
        string='status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False
    )
    price = fields.Char(required=True)
    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="property"
    )
    validity = fields.Float(default=7)
    deadline = fields.Date(compute="_compute_validity", inverse="_inverse_deadline", default=fields.Datetime.now() + relativedelta(days=7))

    @api.depends("validity")
    def _compute_validity(self):
        for record in self:
            record.deadline = fields.Datetime.now() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.deadline - fields.datetime.now().date()).days
