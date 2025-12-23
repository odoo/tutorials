import { registry } from "@web/core/registry";
import { useService, useOwnedDialogs } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { Component, useState } from "@odoo/owl";
import { DashboardItem } from "./dashboard-item/dashboard-item";
import { NumberCard } from "./number-card/number-card";
import { PieChartCard } from "./pie-chart/pie-chart-card";
import { DashboardDialog } from "./configuration-dialog/configuration-dialog";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, NumberCard, PieChartCard };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.configDialog = useOwnedDialogs();

        // Dashboard items
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            disabledItems: JSON.parse(
                browser.localStorage.getItem("awesome_dashboard.disabled") ?? "[]"
            ),
        });
    }

    actionCustomers() {
        this.action.doAction("base.action_partner_form", { viewType: "kanban" });
    }

    actionLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    updateConfiguration(disabledItems) {
        browser.localStorage.setItem("awesome_dashboard.disabled", JSON.stringify(disabledItems));
        this.state.disabledItems = disabledItems;
    }

    openDashboardConfig() {
        this.configDialog(DashboardDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            updateConfiguration: this.updateConfiguration.bind(this),
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
