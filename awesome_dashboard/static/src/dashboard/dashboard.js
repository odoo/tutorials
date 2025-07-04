/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { DashboardItem } from "./components/dashboard_item";
import { PieChart } from "./components/pie_chart";
import "./dashboard_items.js";
import "./services/statistics.js";
import { showDialog } from "@web/core/dialog/dialog";
import { DashboardSettingsDialog } from "./components/dashboard_settings_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };
    setup() {
        this.action = useService("action");
        const { statistics } = useService("awesome_dashboard.statistics");
        this.state = useState(statistics);

        const itemRegistry = registry.category("awesome_dashboard_items");
        const allItems = itemRegistry.getAll();

        const hiddenIds = JSON.parse(localStorage.getItem("awesome_dashboard.hidden_items") || "[]");
        this.items = allItems.filter((item) => !hiddenIds.includes(item.id));

        this.dialog = useService("dialog");
    }


    openLeadsView() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }

    openSettingsDialog() {
        this.dialog.add(DashboardSettingsDialog, {
            onClose: () => { },
        });
    }

}

registry.category("lazy_components").add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);