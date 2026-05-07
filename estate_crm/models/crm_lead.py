from odoo import models, fields


class CrmLead(models.Model):
    _inherit = "crm.lead"

    offer_ids = fields.Integer()