import { Component, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { loadBundle } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
        onSliceClick: { type: Function, optional: true },
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(async () => {
            await loadBundle("web.chartjs_lib");
        });

        useEffect(() => {
            this.renderChart();
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const data = this.props.data;
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(data).map((k) => k.toUpperCase()),
                datasets: [{ data: Object.values(data) }],
            },
            options: {
                responsive: true,
                onClick: (ev) => this.onChartClick(ev),
                plugins: {
                    legend: { position: "bottom" },
                },
            },
        });
    }

    onChartClick(ev) {
        if (!this.props.onSliceClick) {
            return;
        }
        const [activeElement] = this.chart.getElementsAtEventForMode(
            ev,
            "nearest",
            { intersect: true },
            false
        );
        if (!activeElement) {
            return;
        }
        const label = this.chart.data.labels[activeElement.index];
        this.props.onSliceClick(label.toLowerCase());
    }
}
