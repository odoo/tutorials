import {Component, onWillStart, onWillUnmount, useEffect, useRef} from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_owl.pie_chart";
    static props = {
        dataset: {
            type: Object
        },
    };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderChart());
        onWillUnmount(this.onWillUnmount);
    }

    destroyChart() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    onWillUnmount() {
        this.destroyChart();
    }

    renderChart() {
        this.destroyChart();
        const config = this.getChartConfig();
        this.chart = new Chart(this.canvasRef.el, config);
    }

    getChartConfig() {
        const labels = Object.keys(this.props.dataset);

        const data = Object.values(this.props.dataset);

        return {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [
                    {
                        data: data,
                    }
                ],
            }
        };
    }

}
