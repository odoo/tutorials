from odoo.exceptions import UserError

from odoo import fields, models, api


class RealEstatePropertiesMaintenanceRequest(models.Model):
    _name = 'real.estate.property.maintenance.request'
    _description = 'Real Estate Property Maintenance Request'

    name = fields.Char()
    cost = fields.Integer()
    status = fields.Selection([
        ('new', 'New'),
        ('approved', 'Approved'),
        ('done', 'Done'),
    ], string="Status", copy=False, default='new')
    property_id = fields.Many2one('real.estate', string='Property', ondelete='restrict')

    @api.onchange('status')
    def _check_cost_on_accepted_status(self):
        if self.status == 'approved' and self.cost <= 0:
            raise UserError("Approved cost must be greater than 0")

    # @api.constrains('cost', 'status')
    # def _check_cost(self):
    #     invalid_records = self.filtered(
    #         lambda r: r.status == 'approved' and r.cost <= 0
    #     )
    #     if invalid_records:
    #         raise UserError('Approved cost must be greater than 0')

    @api.ondelete(at_uninstall=False)
    def _unlink_if_maintenance_request_not_done(self):
        maintenace_request = self.filtered_domain([('status', '!=', 'done')])
        if maintenace_request:
            raise UserError("Can't delete an active Maintenance Request Record!")
