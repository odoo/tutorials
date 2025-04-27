from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    receipt_layout = fields.Selection([
        ('light', 'Light'),
        ('lined', 'Lined'),
        ('boxed', 'Boxed')
    ], string="Receipt Layout", default='light')

    receipt_header = fields.Html(string="Header")
    receipt_footer = fields.Html(string="Footer")
    receipt_logo = fields.Binary(string="Logo")
    receipt_rendered_template = fields.Html("Final Rendered Receipt Template", sanitize=False)

    def compute_receipt_rendered_template(self):
        for config in self:
            if config.receipt_layout == 'light':
                template = 'pos_receipt_layout_customization.receipt_light_template'
            elif config.receipt_layout == 'lined':
                template = 'pos_receipt_layout_customization.receipt_lined_template'
            elif config.receipt_layout == 'boxed':
                template = 'pos_receipt_layout_customization.receipt_boxed_template'
            else:
                template = False

            if template:
                config.receipt_rendered_template = self.env['ir.ui.view']._render_template(
                    template,
                    {
                        'header_html': config.receipt_header,
                        'footer_html': config.receipt_footer,
                        'logo': config.receipt_logo,
                        'is_restaurant': config.module_pos_restaurant,
                        # 'company': config.company_id,
                    }
                )
            else:
                config.receipt_rendered_template = "<p>No Template Available</p>"
