from odoo import models,fields 

class PosOrder(models.Model): 
    _inherit = "pos.order"
    sales_person_id=fields.Many2one("hr.employee",string="Salesperson")
    