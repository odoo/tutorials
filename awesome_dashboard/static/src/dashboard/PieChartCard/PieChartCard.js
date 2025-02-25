import { Component} from "@odoo/owl";
import { PieChart } from "../PieChart/PieChart";
export class PieChartCard extends Component {
    static template = 'awesome_dashboard.pieChartCard';
    static props = ['title', 'data'];
    static components ={PieChart}
  }
  