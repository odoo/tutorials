import { Component } from "@odoo/owl";
import { PieChart } from "../PieChart/PieChart";


export class ChartCard extends Component {
    static template = "awesome_dashboard.ChartCard";
    static components = { PieChart};
    static props = {
        title: String,
        label : String,
        data : {type : Object, optional: true},
    }
}
