/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { DashboardItem } from "./dashboard_item.js";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { PieChart } from "./piechart.js"; 


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.data); 
        this.action = useService("action");

        this.layoutProps = { controlPanel: {} };

        // onWillStart(async () => {
        //     const result = await this.statisticsService.loadStatistics(); 
        //     Object.assign(this.statistics, result); 
        //     console.log("Loaded statistics:", this.statistics);
        // });
    }
   

    openSettings() {
        this.action.doAction("base_setup.action_general_configuration");
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);

