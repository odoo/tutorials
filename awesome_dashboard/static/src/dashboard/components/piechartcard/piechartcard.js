import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class PiechartCard extends Component{
    static template = "awesome_dashboard.piechartCard";
    static components = { PieChart }
    static props = {
        desc : String,
        value : Object
    }
}
