import { Component, useRef, onWillStart, useEffect, onWillUnmount } from "@odoo/owl";
import { getColor } from "@web/core/colors/colors";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        salesData: {
            type: Object,
            shape: {
                m: Number,
                s: Number,
                xl: Number
            }
        },
        chartLabel: String
    }
    
    setup() {
        this.canvasRef = useRef('canvas');
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderChart());
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
        const ctx = this.canvasRef.el.getContext('2d');
        this.chart = new Chart(ctx, this.getChartConfig());
    }

    getChartConfig() {
        const labels = Object.keys(this.props.salesData);
        const data = Object.values(this.props.salesData);
        const color = labels.map((_, index) => getColor(index));
        return {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.chartLabel,
                        data: data,
                        backgroundColor: color
                    },
                ],
            },
        };
    }
};
