# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_so_perm = fields.Boolean(string="Show Sales Orders", default=True)
    is_quotes_perm = fields.Boolean(string="Show Quotations", default=True)
    is_rfq_perm = fields.Boolean(string="Show Request for Quotation", default=True)
    is_po_perm = fields.Boolean(string="Show Purchase Orders", default=True)
    is_invoices_perm = fields.Boolean(string="Show Invoices & Bills", default=True)
    is_projects_perm = fields.Boolean(string="Show Projects", default=True)
    is_tasks_perm = fields.Boolean(string="Show Tasks", default=True)
