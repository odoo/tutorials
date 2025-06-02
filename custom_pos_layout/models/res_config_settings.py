from odoo import api,fields, models 

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    """pos_disp_type = fields.Selection([  
        ('default', 'Default'),
        ('lined', 'Lined'),
        ('boxed', 'Boxed'),
    ],string="POS Recipt Layout",config_parameter="pos.receipt_layout")"""

    pos_disp_type = fields.Selection([
        ('default', 'Default'),
        ('lined', 'Lined'),
        ('boxed', 'Boxed'),
    ],string="POS Recipt Layout",compute='_compute_disp_type',inverse='_set_disp_type',store=True,readonly=False)

    @api.depends('pos_config_id')
    def _compute_disp_type(self):
        for res_config in self:
            res_config.pos_disp_type = res_config.pos_config_id.pos_disp_type
        print("COmpute is called")
    
    def _set_disp_type(self):
        """Write the selected value back to pos.config"""
        for res_config in self:
            if res_config.pos_config_id:
                res_config.pos_config_id.pos_disp_type = res_config.pos_disp_type

    def action_open_receipt_preview_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'POS Receipt Preview',
            'res_model': 'pos.receipt.preview.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.ids},
        }

class PosConfig(models.Model):
    _inherit='pos.config'

    pos_disp_type = fields.Selection([  
        ('default', 'Default'),
        ('lined', 'Lined'),
        ('boxed', 'Boxed'),
    ],string="POS Recipt Layout",store=True)
