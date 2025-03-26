/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from '@web/search/layout';
import { useService } from '@web/core/utils/hooks';
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboarditem/dashboard_item";
import { PieChart } from "./piechart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart }

    setup(){
       this.action = useService("action");
       const statisticsService = useService("awesome_dashboard.statistics");
    //    this.statistics = useState({
    //         average_quantity: 0,
    //         average_time: 0,
    //         nb_cancelled_orders: 0,
    //         nb_new_orders: 0,
    //         total_amount: 0,
    //         orders_by_size: [],
    //     });
        this.statistics = useState(statisticsService.statistics);

        // onWillStart(async () => {
        //     const result = await this.statisticsService.loadStatistics();
        //     Object.assign(this.statistics, result);
        //     console.log(result);

        // });

    }

    openCustomersKanban(){
        this.action.doAction("base.action_partner_form");
    }

    async openCrmLead(crm){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('CRM Lead'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'],[false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
