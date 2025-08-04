/** @odoo-module **/

import { Component, onMounted, onWillStart, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        "data": { type: Object, optional: true },
        "title": { type: String, optional: true },
        "onSectionClick": { type: Function, optional: true },
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;
        this.chartReady = false;

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            this.chartReady = true;
        });

        onMounted(() => {
            if (this.chartReady) {
                this.renderChart();
            }
        });
    }

    renderChart() {
        if (!this.canvasRef.el || !this.props.data || !window.Chart) return;

        const ctx = this.canvasRef.el.getContext('2d');
        
        // Prepare data for Chart.js
        const labels = Object.keys(this.props.data);
        const values = Object.values(this.props.data);
        const colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
        ];

        this.chart = new window.Chart(ctx, {
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
                onClick: (event, elements) => {
                    if (elements.length > 0 && this.props.onSectionClick) {
                        const elementIndex = elements[0].index;
                        const selectedSize = labels[elementIndex];
                        this.props.onSectionClick(selectedSize);
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    title: {
                        display: !!this.props.title,
                        text: this.props.title,
                        font: {
                            size: 16,
                            weight: 'bold'
                        },
                        padding: 20
                    }
                },
                // Add cursor pointer to indicate clickable sections
                onHover: (event, elements) => {
                    event.native.target.style.cursor = elements.length > 0 ? 'pointer' : 'default';
                }
            }
        });
    }

    willUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }
}
