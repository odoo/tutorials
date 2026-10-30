import { Component, usePlugin } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { ActionPlugin } from "@web/webclient/actions/action_plugin";
import { DashboardItem } from "./dashboard_item";
import { ReportingPlugin } from "./reporting_plugin";
import { dashboardItems } from "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    items = dashboardItems.items;

    action = usePlugin(ActionPlugin);
    reporting = usePlugin(ReportingPlugin);

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
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
}

registry.category("lazy_components").add("Dashboard", AwesomeDashboard);
