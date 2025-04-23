from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate offer model"

    price = fields.Float()
    status = fields.Selection(copy=False,
                              selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    creation_date = fields.Date(readonly=True, default=lambda self: self._current_day())  # To fix the creation date
    validity = fields.Integer(string="Validity (days)", default=7)  # Default validity days
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # Many2One relationships
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    # ---------------
    # Compute methods
    # ---------------

    def _current_day(self):
        return fields.Date.today()

    @api.depends('creation_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.creation_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.creation_date).days
