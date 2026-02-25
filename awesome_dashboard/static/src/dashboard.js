import { Component, onWillStart, useEffect, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboardItem";
import { PieChart } from "./pie_chart/pieChart"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        const statistics = useService("statistics");

        this.statisticsData = useState(statistics.data);


        const updateData = ((data) => {
            this.result = data

            this.data = Object.entries(data.orders_by_size).map(([key, value]) => ({
                label: key, 
                value: value
            }));
        }).bind(this)

        onWillStart(() => {
            updateData(this.statisticsData.statistics)
        })

        useEffect(updateData, () => [this.statisticsData.statistics])
    }
    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads(){
        this.action.doAction({
            type: "ir.actions.act_window",
            views: [[false, "list"], [false, 'form']],
            res_model: "crm.lead",
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
