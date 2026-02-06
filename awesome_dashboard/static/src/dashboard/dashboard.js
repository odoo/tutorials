import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.stateService = useService("awesome_dashboard.statistics");
        this.state = useState({
            statistics: { data: {} }
        });
        onWillStart(async () => {
            const stats = await this.stateService.loadStatistics();
            if (stats) {
                this.state.statistics.data = stats;
            }
        });
    }
    opencustomers() {
        this.action.doAction("base.action_partner_form")
    }
    openlead() {
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
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
