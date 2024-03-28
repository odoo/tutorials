/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart";
import { ConfigDialog } from "./config_dialog";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, Layout, PieChart };

    setup() {
        this.rpc = useService("rpc");
        this.dialog = useService("dialog");
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));

        this.items = registry.category("awesome_dashboard").getAll();

        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || [],
        });
    }

    openConfiguration() {
        this.dialog.add(ConfigDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        });
    }

    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            target: "current",
            res_id: "crm_lead_all_leads_view_tree",
            res_model: "crm.lead",
            views: [[false, "tree"], [false, "kanban"]],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
