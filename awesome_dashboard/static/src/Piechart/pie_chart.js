/** @odoo-module **/

import { Component, onWillStart, onMounted, onWillUnmount, useRef } from '@odoo/owl';
import { loadJS } from '@web/core/assets';
import { rpc } from '@web/core/network/rpc';

export class PieChart extends Component {
    static template = 'awesome_dashboard.PieChart';

    setup() {
        this.canvasRef = useRef('canvas');
        this.chartInstance = null; 
        this.intervalId = null; 

        onWillStart(async () => {
            await loadJS('/web/static/lib/Chart/Chart.js');
            this.chartData = await rpc('/awesome_dashboard/statistics');
        });

        onMounted(() => {
            this.initializeChart();
            this.intervalId = setInterval(() => {
                this.updateChart();
            }, 1000);
        });

        onWillUnmount(() => {
            if (this.intervalId) {
                clearInterval(this.intervalId);
            }
            if (this.chartInstance) {
                this.chartInstance.destroy(); 
            }
        });
    }

    initializeChart() {
        if (this.canvasRef.el && window.Chart) {
            const ctx = this.canvasRef.el.getContext('2d');
            this.chartInstance = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ["S", "M", "L", "XL", "XXL"],
                    datasets: [{
                        data: [
                            this.chartData.orders_by_size.s || 0,
                            this.chartData.orders_by_size.m || 0,
                            this.chartData.orders_by_size.l || 0,
                            this.chartData.orders_by_size.xl || 0,
                            this.chartData.orders_by_size.xxl || 0,
                        ],
                        backgroundColor: ["#ff6384", "#36a2eb", "#ffce56", "#4bc0c0", "#9966ff"],
                    }],
                },
            });
        }
    }

    async updateChart() {
        const newData = await rpc('/awesome_dashboard/statistics');
        if (this.chartInstance && newData) {
            this.chartInstance.data.datasets[0].data = [
                newData.orders_by_size.s || 0,
                newData.orders_by_size.m || 0,
                newData.orders_by_size.l || 0,
                newData.orders_by_size.xl || 0,
                newData.orders_by_size.xxl || 0,
            ];
            this.chartInstance.update(); 
        }
    }
}
