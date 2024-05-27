/** @odoo-module **/

import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useOwnedDialogs, useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { useDashboardConfig, useStatistics } from "../../hooks";
import { DashboardConfigDialog } from "../dashboard_config/dashboard_config_dialog";
import { DashboardItem } from "../dashboard_item/dashboard_item";
import { PieChart } from "../pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, Layout, PieChart };

    setup() {
        this.actionService = useService("action");
        this.statistics = useStatistics();
        this.dashboardConfig = useDashboardConfig();
        this.openDialog = useOwnedDialogs();

        this.items = registry.category("awesome_dashboard").getAll();
    }

    openCustomers() {
        this.actionService.doAction("base.action_partner_form");
    }

    openLeads() {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'tree'], [false, 'form']],
        });
    }

    openSettingsDialog() {
        this.openDialog(DashboardConfigDialog);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
