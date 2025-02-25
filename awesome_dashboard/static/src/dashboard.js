/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";


class AwesomeDashboard extends Component {
    static components = { Layout, DashboardItem, PieChart };
    static template = "awesome_dashboard.AwesomeDashboard";

    setup(){
        this.action = useService("action");
        this.state = useState({ statistics: [], test: {} });
        this.serviceStats = useService("statistics");

        onWillStart(async () => {
            /*const data = await this.serviceStats.loadStatistics();
            console.log(data);
            if(!data.orders_by_size.hasOwnProperty("datasets")){
                data.orders_by_size = {
                    datasets: [{
                        data: [
                            data.orders_by_size.m,
                            data.orders_by_size.s,
                            data.orders_by_size.xl
                        ]
                    }],
                    labels: ['m', 's', 'xl']
                };
            }*/
            this.state.test = await this.serviceStats.loadStatistics();
            console.log(this.state.test);
            if(!this.state.test.orders_by_size.hasOwnProperty("datasets")){
                this.state.test.orders_by_size = {
                    datasets: [{
                        data: [
                            this.state.test.orders_by_size.m,
                            this.state.test.orders_by_size.s,
                            this.state.test.orders_by_size.xl
                        ]
                    }],
                    labels: ['m', 's', 'xl']
                };
            }
            this.state.statistics = this.state.test;
        });
    }

    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }

    async openLeads(activity){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_id: activity.res_id,
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']]
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
