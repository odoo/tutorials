import { onWillStart, useRef, onMounted, useEffect, Component } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = { data: { type: Object } };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this._renderChart();
        });

        useEffect(() => {
            this._updateChart();
        }, () => [this.props.data]);
    }

    _renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["M", "S", "XL"],
                datasets: [{
                    data: [
                        this.props.data.m || 0,
                        this.props.data.s || 0,
                        this.props.data.xl || 0
                    ],
                    backgroundColor: ["#fff71b", "#15ff00", "#1b94ff"]
                }],
            },
        });
    }

    _updateChart() {
        if (this.chart) {
            this.chart.data.datasets[0].data = [
                this.props.data.m || 0,
                this.props.data.s || 0,
                this.props.data.xl || 0
            ];
            this.chart.update();
        }
    }
}