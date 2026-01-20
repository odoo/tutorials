/** @odoo-module **/

import { Component, useState, useEffect } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardCard } from "./dashboard_card";
import { statisticService } from "./statistic_service";
import { PieChart } from "./pie_chart";

registry.category("services").add("statisticService", statisticService);

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardCard, PieChart }

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("statisticService")
        
        const { stats } = useService("statisticService");

        this.stats = useState(stats);

        useEffect(() => {
            console.log(this.stats)
        })
    }

    openCustomersDashboard() {
        this.action.doAction("base.action_partner_form");
    }

    async openLeadsDashboard() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            views: [[false, "list"], [false, "form"]],
            view_mode: "list,form",
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);




