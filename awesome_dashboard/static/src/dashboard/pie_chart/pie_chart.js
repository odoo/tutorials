import { Component, useEffect, useRef, onWillStart } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { loadJS } from "@web/core/assets";

const D3_COLORS = [
    "#1f77b4",
    "#ff7f0e",
    "#aec7e8",
    "#ffbb78",
    "#2ca02c",
    "#98df8a",
    "#d62728",
    "#ff9896",
    "#9467bd",
    "#c5b0d5",
    "#8c564b",
    "#c49c94",
    "#e377c2",
    "#f7b6d2",
    "#7f7f7f",
    "#c7c7c7",
    "#bcbd22",
    "#dbdb8d",
    "#17becf",
    "#9edae5",
];

export class PieChart extends Component {
    static components = { Layout };
    static template = "awesome_dashboard.PieChart";

    static defaultProps = {
        s: 0,
        m: 0,
        l: 0,
        xl: 0,
        xxl: 0,
    };

    setup() {
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        this.canvasRef = useRef("canvas");
        useEffect(() => this.renderChart());
    }

    destroyChart() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    renderChart() {
        this.destroyChart();
        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx, this.getChartConfig());
    }

getChartConfig() {
    const data = this.props.data || {}; 
    const labels = Object.keys(data);
    const counts = Object.values(data);

    return {
        type: "pie",
        data: {
            labels: labels, 
            datasets: [
                {
                    data: counts, 
                    backgroundColor: labels.map((_, index) => D3_COLORS[index % 20]),
                    hoverOffset: 4
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                }
            }
        },
    };
}
}
