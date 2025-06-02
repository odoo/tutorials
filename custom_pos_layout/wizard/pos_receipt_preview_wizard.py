from odoo import models, fields, api

class POSReceiptPreviewWizard(models.TransientModel):
    _name = 'pos.receipt.preview.wizard'
    _description = 'POS Receipt Preview Wizard'

    pos_disp_type = fields.Selection([  
        ('default', 'Default'),
        ('lined', 'Lined'),
        ('boxed', 'Boxed'),
    ], string="POS Receipt Layout")

    logo_image = fields.Image("Logo")
    receipt_header = fields.Text(string='Receipt Header', help="A short text that will be inserted as a header in the printed receipt.")
    receipt_footer = fields.Text(string='Receipt Footer', help="A short text that will be inserted as a footer in the printed receipt.")
    preview = fields.Html(compute='_compute_preview', sanitize=False)

    @api.onchange('receipt_header','pos_disp_type','receipt_footer','logo_image')
    def _compute_preview(self):
        for wizard in self:
            context = {
                'logo': wizard.logo_image,
                'header': wizard.receipt_header,
                'footer': wizard.receipt_footer,
                'pos_disp_type': wizard.pos_disp_type,
            }
            rendered_html = wizard.env['ir.ui.view']._render_template(
                wizard._get_preview_template(),
                context
            )
            wizard.preview = rendered_html
        
    def _get_preview_template(self):
        return 'custom_pos_layout.external_layout_report'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        id = self.env.context.get('active_id')
        settings_config_id = self.env['res.config.settings'].browse(id)
        res['pos_disp_type']  = settings_config_id.pos_config_id.pos_disp_type
        res['logo_image'] = self.env.company.logo
        return res

    def action_confirm(self):
        self.env.company.logo = self.logo_image
        id = self.env.context.get('active_id')
        settings_config_id = self.env['res.config.settings'].browse(id)
        settings_config_id.pos_config_id.write({
            'pos_disp_type' : self.pos_disp_type,
            'receipt_header': self.receipt_header,
            'receipt_footer': self.receipt_footer
        })   
