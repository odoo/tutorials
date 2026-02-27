import { Component, onWillUnmount, useEffect, useRef, onWillStart } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        label: {type: String, optional: true},
        data: { type: Array, element:{
            type: Object, shape: {label: String, value: Number }
        } },
    };

    setup() {
        this.canvasRef = useRef("canvas");

        this.chart = null;

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));

        useEffect(() => this.renderChart());
        onWillUnmount(this.onWillUnmount);
    }

    onWillUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    getChartConfig() {
        return {
            type: "doughnut",
            data: {
                datasets: [{
                    data: this.props.data.map((element) => element.value),
                    label: this.props.label
                }],
                labels: this.props.data.map((element) => element.label),
            }

        }
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const config = this.getChartConfig();
        this.chart = new Chart(this.canvasRef.el, config);
    }
}