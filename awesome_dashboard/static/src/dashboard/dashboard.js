import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { AwesomeDashboardItem } from "./dashboard_item";
import { rpc } from "@web/core/network/rpc";
import { PieChart } from "./pie_chart";

class AwesomeDashboard extends Component {
    static components = { AwesomeDashboardItem, PieChart, Layout };
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard.statistics"));

        onWillStart(async () => {
            const res = await rpc("/awesome_dashboard/statistics");
            console.log(res);
            Object.assign(this.stats, res);
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "form"],
                [false, "list"],
            ],
        });
    }
}

registry
    .category("lazy_components")
    .add("AwesomeDashboard", AwesomeDashboard);
