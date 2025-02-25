import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart";
import { dashboardItems } from "./dashboard_items"


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem , PieChart };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("statistics");
        this.stats = useState(this.statisticsService.stats);
        this.items= registry.category("awesome_dashboard").getAll();

        /*onWillStart(async () => {
            this.stats = await this.statisticsService.loadStatistics();
            console.log(this.stats);
        });*/
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            target: "current",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

/* const myService = {
    dependencies: ["notification"],
    start(env, { notification }) {
        let counter = 1;
        setInterval(() => {
            notification.add(`Tick Tock ${counter++}`);
        }, 1000);
    },
};

registry.category("services").add("myService", myService); */

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
