from odoo import api, fields, models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"
    
    service_employee_id = fields.Many2one('hr.employee', string='Service Employee', help="Select the employee per orderline")
    
    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields.append("service_employee_id")
        return fields
