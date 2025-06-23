/** @odoo-module **/

import { Component, useState, onWillStart} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { PieChart } from "./piechart/piechart";
import { DashboardItem } from "./dashboarditem/dashboarditem";
import { PieChartCard } from "./piechartcard/piechartcard";
import { NumberCard } from "./numbercard/numbercard";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem ,PieChart,PieChartCard,NumberCard};

    setup() {
        const dashboardItemsRegistry = registry.category("awesome_dashboard");
        this.items = dashboardItemsRegistry.getAll();
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statistics.stats);
        console.log("AwesomeDashboard setup", this.state);
    }
    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }
    async openLeads(){
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
