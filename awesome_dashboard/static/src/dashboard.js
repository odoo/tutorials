/** @odoo-module **/

import {Component, onWillStart} from "@odoo/owl";
import {Layout} from "@web/search/layout";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {DashboardItem} from "./dashboard_item/dashboard_item";
import {loadJS} from "@web/core/assets";
import {PieChart} from "./piechart/piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart};

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.myact = useService("action");
        this.myservice = useService("awesome_dashboard.statistics");
        onWillStart(async () => {
            this.result = await this.myservice.loadStatistics();
            this.orderSize=this.result["orders_by_size"];
            delete this.result["orders_by_size"];
            console.log(this.result);
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

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
