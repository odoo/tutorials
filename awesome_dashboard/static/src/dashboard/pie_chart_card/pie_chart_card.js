/** @odoo-module */

import { Component } from "@odoo/owl";
import { user } from "@web/core/user";
import { useService } from "@web/core/utils/hooks";
import { PieChart } from "../pie_chart/pie_chart";


export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        title: {
            type: String,
        },
        values: {
            type: Object,
        },
    };

    setup(){
        this.orm = useService("orm");
    }

    async saveChartData(){
        await this.orm.call("res.users", "set_statistics", [
            user.userId,
            this.props.values,
        ]);
    }
}
