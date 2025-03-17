# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command
from . import models
from . import controllers
from . import tests


def set_menu_visibility_for_kiosk(env):
    """Set visibility of menus to show only kiosk app for internal users."""
    menus = env['ir.ui.menu'].search([])
    internal_user_group = env.ref('base.group_user')
    system_admin_group = env.ref('base.group_system')
    kiosk_root_menu = env.ref('time_tracking_kiosk.menu_timesheet_kiosk_root')
    kiosk_mode_menu = env.ref('time_tracking_kiosk.menu_timesheet_kiosk_mode')

    for menu in menus:
        if menu.id in [kiosk_root_menu.id, kiosk_mode_menu.id]:
            menu.groups_id = [Command.set([internal_user_group.id, system_admin_group.id])]
        else:
            menu.groups_id = [Command.set([system_admin_group.id])]
