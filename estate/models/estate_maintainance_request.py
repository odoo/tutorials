from odoo import api, models, fields


class EstateMaintainanceRequest(models.Model):
    _name = 'estate.maintainance.request'
    _description = 'table for the technician maintainance request'

    property_id = fields.Many2one('estate.property', required=True, readonly=True)
    buyer_id = fields.Many2one('res.users', required=True, default='self.env.uid')
    technician_id = fields.Many2one('res.partner', required=False)
    state = fields.Selection(
        string='state',
        default='new',
        selection=[
            ('new', "New"),
            ('assigned', "Assigned"),
            ('inprogress', "Inprogress"),
            ('done', "Done"),
            ('cancelled', "Cancelled"),
        ],
    )
    estimate_cost = fields.Float(required=False)
    actual_cost = fields.Float(compute='_compute_actual_cost', store=True)
    current_stage = fields.Char(compute='_compute_state_after_assigned', store=True)

    @api.depends('state', 'estimate_cost')
    def _compute_actual_cost(self):
        if self.state == 'done':
            self.actual_cost = self.estimate_cost * 1.18

    @api.depends('technician_id', 'state')
    def _compute_state_after_assigned(self):
        if self.state == 'new' and self.technician_id:
            self.state = 'assigned'
            self.current_stage = 'assigned'
        else:
            self.current_stage = self.state
