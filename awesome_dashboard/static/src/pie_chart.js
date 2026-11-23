import { Component, onWillStart, signal, types as t, useEffect, useProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

const SIZE_COLORS = {
    s: "#36A2EB",
    m: "#FF6384",
    l: "#4BC0C0",
    xl: "#FF9F40",
    xxl: "#9C6DF4",
};

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    props = useProps({
        label: t.string(),
        data: t.object(),
    });

    canvasRef = signal.ref();

    setup() {
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => {
            const canvas = this.canvasRef();
            if (canvas) {
                const chart = this.renderChart(canvas);
                return () => chart.destroy();
            }
        });
    }

    renderChart(canvas) {
        const keys = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = keys.map((key) => SIZE_COLORS[key]);
        return new Chart(canvas, {
            type: "pie",
            data: {
                labels: keys,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: color,
                    },
                ],
            },
            options: {
                maintainAspectRatio: false,
            },
        });
    }
}
