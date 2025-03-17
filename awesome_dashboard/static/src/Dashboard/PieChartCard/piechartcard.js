import { Component } from "@odoo/owl";
import { Piechart } from "../PieChart/piechart"; 

export class PieChartCard extends Component{
    static template = "awesome_dashboard.PieChartCard";
    static components = { Piechart }
    static props = {
        title: {
            type: String,
        },
        value: {
            type: Object,
        },
    }
}
