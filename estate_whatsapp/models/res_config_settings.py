from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # def _default_company(self):
    #     return self.env['res.company'].company_id, limit=1)

    company_id = fields.Many2one(
        'res.company',
        string="company",
        ondelete='cascade')
    wa_sale_template_id = fields.Many2one(related='company_id.wa_sale_template_id', readonly=False, store=True)
