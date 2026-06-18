# -*- coding: utf-8 -*-
from odoo import models

class AccountReport(models.Model):
    _inherit = 'account.report'

    def _init_options_preview_before_export(self, options, previous_options):
        options['preview_before_export'] = True
