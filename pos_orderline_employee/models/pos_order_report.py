from odoo import models, fields


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"
    
    service_employee_id = fields.Many2one('hr.employee', string='Service Employee', readonly=True)
    total_order_lines = fields.Integer(string='Total Orderlines', readonly=True)

    def _select(self):
        return super()._select() + """
            , l.service_employee_id AS service_employee_id
            , (SELECT COUNT(*) 
               FROM pos_order_line pol 
               WHERE pol.id = l.id) AS total_order_lines
        """
