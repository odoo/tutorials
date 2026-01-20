/** @odoo-module **/

import { useState, Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { ConfigurationDialog } from "./ConfigurationDialog/configuration_dialog";
import { PieChart } from "./PieChart/pie_chart";
import { DashboardItem } from "./dashboard_item";
import { browser } from "@web/core/browser/browser";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, ConfigurationDialog };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.statistics);
        this.items = registry.category("awesome_dashboard").getAll();

        this.dialog = useService("dialog");
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }

    openDialog() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }

    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
