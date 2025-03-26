from odoo import api, fields, models


class ReceiptsLayout(models.TransientModel):
    _name = 'receipts.layout'
    _description = 'POS Receipt Layout'

    def _get_default_pos_config(self):
        return self.env['pos.config'].browse(self.env.context.get('active_pos_config_id'))

    pos_config_id = fields.Many2one('pos.config', string='Point of Sale', default=_get_default_pos_config, required=True)
    receipt_layout = fields.Selection(related='pos_config_id.receipt_layout', readonly=False, required=True)
    receipt_logo = fields.Binary(related='pos_config_id.receipt_logo', readonly=False)
    receipt_header = fields.Html(related='pos_config_id.receipt_header', readonly=False)
    receipt_footer = fields.Html(related='pos_config_id.receipt_footer', readonly=False)
    preview = fields.Html(compute='_compute_receipt_preview')

    def receipt_layout_save(self):
        return {'type': 'ir.actions.act_window_close'}

    @api.depends('receipt_layout','receipt_header','receipt_footer','receipt_logo')
    def _compute_receipt_preview(self):
        """ Compute a QWeb-based preview to display on the wizard """
        for wizard in self:
            if wizard.pos_config_id:
                wizard.preview = wizard.env['ir.ui.view']._render_template(
                    wizard._get_receipt_preview_template(),{
                        'receipt_header': wizard.receipt_header,
                        'receipt_footer': wizard.receipt_footer,
                        'receipt_logo': wizard.receipt_logo,

                    }
                )
            else:
                wizard.preview = False
  
    def _get_receipt_preview_template(self):
        is_restaurant = self.pos_config_id.module_pos_restaurant
        base_module = 'pos_receipt.report_restaurant_preview' if is_restaurant else 'pos_receipt.report_receipts_wizard_preview'
        
        layout_templates = {
            'light': f'{base_module}_light',
            'boxes': f'{base_module}_boxes',
            'lined': f'{base_module}_lined'
        }
        
        return layout_templates.get(self.receipt_layout, layout_templates['light'])
