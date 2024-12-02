/** @odoo-module **/

import {Component} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {Card} from "../../card/card"
import {DashboardItemManager} from "../dashboard_objects";
import {PieChart} from "./pie_chart/pie_chart";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard.dashboard_item";

    static components = {Card, PieChart}

    static props = {
        item: {
            type: DashboardItemManager
        }
    }

    setup() {
        this.stats = useService("awesome_dashboard.statistics").useStatistics()
    }
}
