/** @odoo-module **/
import { Component, onWillStart, onMounted, onWillUnmount, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: { type: Object },
    };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this.renderChart();
        });

        // Re-render chart when data changes
        useEffect(() => {   
            if (this.canvasRef.el) {
                this.renderChart();
            }
        }, () => [this.props.data.orders_by_size]);


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

        const ordersBySizeData = this.props.data?.orders_by_size || {};
        const labels = Object.keys(ordersBySizeData);
        const values = Object.values(ordersBySizeData);
        
        if (labels.length === 0) {
            return;
        }

        const colors = [
            '#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF','#FF9F40'
        ];

        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                labels: labels.map(label => label.toUpperCase()),
                datasets: [{
                    data: values,
                    backgroundColor: colors.slice(0, labels.length),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true,
                            pointStyle: 'rect'
                        }
                    },
                    title: {
                        display: true,
                        text: 'T-Shirt Sales by Size',
                        font: {
                            size: 16,
                            weight: 'bold'
                        },
                        padding: 20
                    }
                }
            }
        });
    }
}