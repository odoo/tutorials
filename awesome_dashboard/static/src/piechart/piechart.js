import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        graphData: {
            type: Object,
        }
    }

    setup() {
        this.canvasRef = useRef('canvas');
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        })
        useEffect(() => {
            this.renderChart();
            return () => this.chart?.destroy();
        });
    }


    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const ctx = this.canvasRef.el.getContext('2d');
        this.chart = new Chart(ctx, this.getChartConfig());
    }

    getChartConfig() {
        if (!this.props.graphData) return {};
        const { labels, data } = Object.entries(this.props.graphData).reduce(
            (acc, [key, value]) => {
                return ({ labels: [...acc.labels, key], data: [...acc.data, value] })
            }, { labels: [], data: [] });
        return {
            type: 'pie',
            data: {
                labels,
                datasets: [
                    {
                        data,
                    }
                ]
            },
            options: {
                aspectRatio: 2,
            }
        }
    }
}
