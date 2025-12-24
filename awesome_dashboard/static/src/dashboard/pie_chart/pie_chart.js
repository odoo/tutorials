import { Component, onWillStart, useRef, useEffect, onWillUnmount } from "@odoo/owl"
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart"
    static props = {
        data: Object
    }

    setup() {
        this.canvaRef = useRef("canvaRef")
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"))
        useEffect(() => this.renderChart());
        onWillUnmount(this.destroyChart);
    }

    destroyChart() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    renderChart() {
        this.destroyChart();
        const ctx = this.canvaRef.el.getContext("2d")
        this.chart = new Chart(ctx, this.getChartConfig())
    }

    getChartConfig() {
        const chartData = this.props.data;
        console.log("chart data in chartconfig", chartData);
        console.log(Object.keys(chartData));
        console.log(Object.values(chartData));

        return {
            type: "pie",
            data: {
                labels: Object.keys(chartData),
                datasets: [{
                    data: Object.values(chartData)
                }]
            }
        }
    }
}