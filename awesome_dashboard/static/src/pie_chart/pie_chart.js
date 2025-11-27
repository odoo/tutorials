import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        pieChartData: Object,
    }

    setup() {
        this.canva = useRef("canva");
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        onMounted( () => this.renderChart() );
    }

    renderChart() {
        const labels = Object.keys(this.props.pieChartData);
        const values = Object.values(this.props.pieChartData);
        this.myPieChart = new Chart(this.canva.el, {
            type: 'pie',
            data: {
                labels,
                datasets: [
                    {
                        data: values,
                    }
                ]
            },
        })
    }

}
