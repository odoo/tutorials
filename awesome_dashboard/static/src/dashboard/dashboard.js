/** @odoo-module **/

import {Component, onWillStart, useState} from "@odoo/owl";
import {Layout} from "@web/search/layout";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {DashboardItem} from "./dashboard_item/dashboard_item";
import {PieChart} from "./piechart/piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart};

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.myact = useService("action");
        this.myservice = useState(useService("awesome_dashboard.statistics"));
        onWillStart(async () => {
        console.log("started dashboard");
        const { orders_by_size, ...rest } = await this.myservice.loadStatistics();
        this.result=rest;
        this.orderSize=orders_by_size;
        console.log(this.orderSize)
        });

    }

    openCustomers() {
        this.myact.doAction("base.action_partner_form");
    }

    openCrm() {
        this.myact.doAction({
            type: 'ir.actions.act_window',
            name: 'Lead',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

}
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);

