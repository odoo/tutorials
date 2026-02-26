from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstateRequest(models.Model):
    _name = "estate.request"
    _description = "Real Estate Request"

    name = fields.Char(required=True)
    description = fields.Text()
    request_date = fields.Date(default=fields.Date.today)
    estimated_price = fields.Float(required=True, default=10000.0)
    actual_price = fields.Float(readonly=True, copy=False)
    request_id = fields.Many2one(
        "estate.property",
        string="Property",
    )
    technician_id = fields.Many2one(
        "res.users",
        string="Technician",
        help="User assigned to handle the maintenance request",
    )
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string="Priority", default='medium')
    state = fields.Selection([
        ('new', "New"),
        ('Assigned', "Assigned"),
        ('Progress', "Progress"),
        ('Done', "Done"),
        ('cancelled', "Cancelled"),
    ], default='new', copy=False)

    @api.onchange('technician_id')
    def _onchange_technician(self):
        for rec in self:
            if rec.technician_id and rec.state == 'new':
                rec.state = 'Assigned'

    @api.onchange('technician_id', 'estimated_price')
    def _onchange_progress(self):
        for rec in self:
            if rec.state == 'Assigned' and rec.technician_id and rec.estimated_price:
                rec.state = 'Progress'

    def action_assign(self):
        for record in self:
            record.state = 'Assigned'

    def action_progress(self):
        for record in self:
            if not record.estimated_price or record.estimated_price <= 0:
                raise ValidationError(
                    "Please fill in the Estimated Price before starting the request."
                )
            record.state = 'Progress'

    def action_done(self):
        for record in self:
            record.state = 'Done'
            record.actual_price = record.estimated_price * 1.20

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'
