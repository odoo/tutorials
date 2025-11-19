from odoo import fields, models, api


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "property offer"

    price = fields.Float(string='Price')
    partner_id = fields.Many2one('res.partner', required=True, string='Partner')
    property_id = fields.Many2one('estate.property', required=True, string='Property')
    date_creation = fields.Date(readonly=True, default=fields.Date.today)
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        string='Deadline', compute="_compute_deadline", inverse="_inverse_deadline"
    )

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                fields.Date.today(), days=record.validity
            )

    @api.onchange('date_deadline')
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days
