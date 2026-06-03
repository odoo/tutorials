import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardSettingsDialog } from "../dashboard_display_settings/dashboard_display_settings";

export class ControlPanelButtons extends Component {
    static template = "awesome_dashboard.control_panel_buttons";

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");


    }

    static props = {
        items: Array,
    };

    redirectToCustomers() {

        this.action.doAction("base.action_partner_form_view1");
    };

    openSettings() {
        this.dialog.add(
            DashboardSettingsDialog,
            {
                items: this.props.items,
            }
        );
    }

    redirectToLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Breadcrumb'),
            target: 'current',
            res_model: 'crm.lead',
            views: [
                [false, 'list']],
        });
    };
}