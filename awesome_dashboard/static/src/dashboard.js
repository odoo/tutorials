import { Component, usePlugin, onWillStart, signal } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { ActionPlugin } from "@web/webclient/actions/action_plugin";
import { DashboardItem } from "./dashboard_item";
import {ReportingPlugin} from "./reporting_plugin";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    action = usePlugin(ActionPlugin);

    reporting = usePlugin(ReportingPlugin)

    statistics = signal(null);

    setup() {
        onWillStart( async () => {
            this.statistics.set(await this.reporting.loadStatistics())
        })
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form")
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
