/** @odoo-module **/

import {Component} from "@odoo/owl";
import {DashboardItem} from "../dashboard_item/dashboard_item";
import {DashboardGridManager} from "../dashboard_objects";

export class DashboardGrid extends Component {
    static template = "awesome_dashboard.awesome_dashboard.dashboard_grid";
    static components = {DashboardItem}

    static props = {
        grid: {
            type: DashboardGridManager
        }
    }

    setup() {
    }
}
