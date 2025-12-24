import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup(){
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");

        this.stats = useState({
            new_orders: 0,
            total_amount: 0,
            avg_tshirt: 0,
            cancelled_orders: 0,
            avg_processing_time: 0,
            sales_by_category: {},
        });
        onWillStart(async() => {
            const result = await this.statistics.loadStatistics();
            Object.assign(this.stats, result);
        });
    }
    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }
    openLeads(){
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            target: "current",
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
