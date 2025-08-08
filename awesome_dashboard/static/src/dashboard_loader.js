import { Component } from "@odoo/owl";
import { LazyComponent } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { Dashboard } from "./dashboard/dashboard";
import { PieChart } from "./dashboard/piechart/piechart";

export class DashboardLoader extends Component {
    static template = 'dashboard_loader.dashboard_loader';
    static components = { Dashboard, LazyComponent }
    setup() {
        this.thing = 'awesome_dashboard.dashboard'
    }
}


registry.category('actions').add('awesome_dashboard.dashboard', DashboardLoader)
