   
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"
   
    wa_sale_template_id = fields.Many2one('whatsapp.template',string='WhatsApp Template', domain=[('model', '=', 'estate.property'), ('status', '=', 'approved')])
