# imports of odoo
from odoo import models


class RecognitionDateSyncWizard(models.TransientModel):
    _inherit = 'account.automatic.entry.wizard'

    def do_action(self):
        """
        Set the date_changed field of the related account move lines
        with the wizard's date, then call the parent method.
        """
        self.env['account.move.line'].browse(self._context.get('active_ids', [])).write({
            'date_changed': self.date
        })

        return super().do_action()
