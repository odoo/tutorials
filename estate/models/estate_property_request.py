from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyRequest(models.Model):
    _name = "estate.property.request"
    _description = "Property Requests"

    technician_id = fields.Many2one(
        'res.partner',
        string='Technician',
        ondelete='restrict',
    )

    request_id = fields.Many2one(
        'estate.property',
        string='Property',
        ondelete='cascade',
    )

    name = fields.Char(required=True)
    description = fields.Text()
    estimated_cost = fields.Float()

    state = fields.Selection(
        [
            ('new', 'New'),
            ('assigned', 'Assigned'),
            ('inprogress', 'In Progress'),
            ('done', 'Done'),
        ],
        default='new',
        string="Status",
    )

    @api.onchange('technician_id')
    def _onchange_technician(self):
        if self.technician_id:
            self.state = 'assigned'
        else:
            self.state = 'new'

    def action_start(self):
        for rec in self:
            if not rec.technician_id:
                message = "Please assign technician first."
                raise UserError(message)
            rec.state = 'inprogress'

    def action_stop(self):
        for rec in self:
            rec.state = 'done'
