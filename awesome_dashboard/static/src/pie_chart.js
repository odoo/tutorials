import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart"
    static props = {
        data: { type: Object, required: true },
    }

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => {
            if (!this.chart) {
                this.renderChart();
            } else {
                this.updateChart();
            }
        },
            () => [this.props.data]
        );
    }

    renderChart() {
        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                datasets: [{data: Object.values(this.props.data)}],
                labels: Object.keys(this.props.data)
            }
        });
    }

    updateChart() {
        if (this.chart) {
            this.chart.data.labels = Object.keys(this.props.data);
            this.chart.data.datasets[0].data = Object.values(this.props.data);
            this.chart.update();
        }
    }

}
