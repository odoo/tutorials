from odoo import models, fields


class CrmLeads(models.Model):
    _inherit = "crm.lead"

    property_id = fields.Many2one("estate.property")
