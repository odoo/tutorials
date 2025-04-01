# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request

class CustomerPortalAccess(CustomerPortal):

    def _prepare_portal_layout_values(self):
        portal_layout_values = super()._prepare_portal_layout_values()
        user = request.env.user
        portal_layout_values.update({
            'is_so_perm': user.is_so_perm,
            'is_quotes_perm': user.is_quotes_perm,
            'is_rfq_perm': user.is_rfq_perm,
            'is_po_perm': user.is_po_perm,
            'is_invoices_perm': user.is_invoices_perm,
            'is_projects_perm': user.is_projects_perm,
            'is_tasks_perm': user.is_tasks_perm
        })
        return portal_layout_values
