import { Component, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation"
import { Layout } from "@web/search/layout"
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart";
import { DashboardConfigDialog } from "./dashboard_config_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem, PieChart, DashboardConfigDialog };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics")
        this.dialog = useService("dialog");
        this.statistics = useState(this.statisticsService);
        this.configState = useState({
            disabledItems: JSON.parse(localStorage.getItem("disabled_dashboard_items") || "[]")
        });
    }

    get items() {
        const allItems = registry.category("awesome_dashboard").getAll();
        return allItems.filter(item => !this.configState.disabledItems.includes(item.id));
    }

    openConfiguration() {
        this.dialog.add(DashboardConfigDialog, {
            onConfigSaved: () => {
                this.configState.disabledItems = JSON.parse(localStorage.getItem("disabled_dashboard_items") || "[]");
            }
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
