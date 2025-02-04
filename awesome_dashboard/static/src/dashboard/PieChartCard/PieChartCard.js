import { Component} from "@odoo/owl";
import { PieChart } from "../PieChart/PieChart";

export class PieChartCard extends Component {
    static template= 'awesome_dashboard.PieChartCard'
    static components= {PieChart}
    static props = {
        title: String,
        labels: Array,
        data: Array
    }
    static defaultProps= {
        labels: [],
        data: []
    }
    super() {
        console.log(this.props)
    }
}