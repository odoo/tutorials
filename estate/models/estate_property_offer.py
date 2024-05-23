from odoo import api, fields, models
from odoo.tools.date_utils import add


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "estate properties offers"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute='_compute_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = add(
                record.create_date or fields.Date.today(), days=record.validity
            )
