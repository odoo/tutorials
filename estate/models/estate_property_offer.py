from odoo import api, models, fields


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "estate property offer"

    price = fields.Float(string='Price')
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(compute="_computed_date_deadline",
                                inverse="_inverse_computed_date_deadline")
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)
    status = fields.Selection(string='Status', copy=False,
                              selection=[
                                  ('accepted', 'Accepted'),
                                  ('refused', 'Refused')
                              ]
                              )
    property_id = fields.Many2one(
        'estate.property', string='Property', required=True)

    @api.depends('create_date', 'validity')
    def _computed_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + record.validity

    @api.depends('date_deadline', 'validity')
    def _inverse_computed_date_deadline(self):
        return
