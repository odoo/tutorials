import { Component, onWillStart, useRef, useEffect, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart"
    static props = {
        label: String,
        data: Object,
    }

    setup() {
        this.canvasRef = useRef('canvas')
        onWillStart(() => {
            return loadJS("/web/static/lib/Chart/Chart.js")
        })
        useEffect(() => this.renderChart());
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        })
    }

    getChartConfig() {
        const { mode } = this.model.metaData;
        let data;
        switch (mode) {
            case "bar":
                data = this.getBarChartData();
                break;
            case "line":
                data = this.getLineChartData();
                break;
            case "pie":
                data = this.getPieChartData();
        }
        const options = this.prepareOptions();
        return { data, options, type: mode };
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const config = {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    label: this.props.label,
                    data: Object.values(this.props.data)

                }],
            }

        };
        this.chart = new Chart(this.canvasRef.el, config);
    }
}