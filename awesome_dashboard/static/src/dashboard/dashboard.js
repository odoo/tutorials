/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";
import { _t } from "@web/core/l10n/translation";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem, PieChart, ConfigurationDialog }

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("statistics");
        this.dialogService = useService("dialog");
        this.statistics = useState(this.statisticsService.statistics)
        this.items = registry.category("awesome_dashboard").getAll();
        const saved = localStorage.getItem("unchecked_ids");
        this.unchecked_ids = useState({ids: saved ? JSON.parse(saved) : []})
    }

    showCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    showLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            res_model: 'crm.lead',
            views: [[false, 'tree'], [false, 'form']],
        });
    }

    onApplied(unchecked_ids) {
        this.unchecked_ids.ids = unchecked_ids.slice()
        console.log(this.unchecked_ids.ids)
    }

    openConfiguration() {
        this.dialogService.add(ConfigurationDialog, {
            onApplied: this.onApplied.bind(this)
        });
    }
}

// registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);