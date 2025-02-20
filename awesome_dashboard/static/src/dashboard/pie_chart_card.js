import { Component, xml } from '@odoo/owl';
import { PieChart } from './pie_chart';

export class PieChartCard extends Component {
    static template = xml`
        <PieChart />
    `;
    static components = { PieChart };
}
