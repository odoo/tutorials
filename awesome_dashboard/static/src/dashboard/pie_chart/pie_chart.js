import { Component, onMounted, onWillStart, onWillUnmount, onWillUpdateProps, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object
    }

    setup() {
        this.canvasRef = useRef("canvas")
        this.actionService = useService("action")

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"))

        onMounted(() => this.renderChart());

        onWillUnmount(() => this.chart?.destroy());

        onWillUpdateProps((nextProps) => {
            if (this.chart) {
                this.chart.data.labels = Object.keys(nextProps.data).map(x => x.toUpperCase());
                this.chart.data.datasets[0].data = Object.values(nextProps.data);
                this.chart.update();
            }
        });
    }

    renderChart() {
        this.chart?.destroy();

        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels.map(x => x.toUpperCase()),
                datasets: [{data}]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const size = labels[index].toLowerCase();
                        this.openOrdersListView(size);
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const label = context.label || "";
                                const value = context.formattedValue;
                                return `${label}: ${value}`;
                            }
                        }
                    }
                },
                hover: {
                    mode: "nearest",
                    intersect: true,
                    onHover: (event, elements) => {
                        canvas.style.cursor = elements.length ? "pointer" : "default";
                    }
                }
            }
        });
    }

    openOrdersListView(size) {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: `Orders with Size ${size.toUpperCase()}`,
            res_model: "sale.order",
            views: [[false, "list"]],
            domain: [["order_line.product_template_attribute_value_ids.display_name", "ilike", size]],
            context: {create: false}
        });
    }
}
