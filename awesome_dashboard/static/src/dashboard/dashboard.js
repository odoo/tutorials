/** @odoo-module **/

import { Component, useState, reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { DashboardConfigDialog } from "./dialog/dialog";
import { Dialog } from "@web/core/dialog/dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, Dialog };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = reactive({ disabledItems: [] });
        this.loadConfig();
    }

    openCustomersKanbanView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    loadConfig() {
        const config = localStorage.getItem("dashboard_hidden_items");
        this.state.disabledItems = config ? JSON.parse(config) : [];
    }

    openConfiguration() {
        this.env.services.dialog.add(DashboardConfigDialog, {
            items: this.items,
            disabledItems: [...this.state.disabledItems],
            onSave: (hiddenItems) => {
                localStorage.setItem("dashboard_hidden_items", JSON.stringify(hiddenItems));
                this.state.disabledItems = hiddenItems;
            },
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
