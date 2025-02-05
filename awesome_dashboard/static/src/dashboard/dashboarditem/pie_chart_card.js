import { Component} from "@odoo/owl";
import { PieChart } from "../chart/pie";
export class PieChartCard extends Component {
    static template= 'awesome_dashboard.PieChartCard'
    
    static props = {
        label: String,
        data: Object,
    };

    static components = {  PieChart };
}