/** @odoo-module **/

import { Component, onWillStart, useRef, onMounted, onWillUnmount,useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets"
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: { type: Object }
    };
    setup() {
        this.chart = null;
        this.canvasRef = useRef("pie_chart_canvas");
        this.action = useService("action");

        onWillStart(async () => await loadJS("/web/static/lib/Chart/Chart.js"))

        useEffect(() => {
            if (this.canvasRef.el) {
                this.drawChart();
            }
        }, () => [this.props.data]);

        onMounted(() => {
            if (this.props.data) {
                this.drawChart();
            }
        });

        onWillUnmount(() => {
        if (this.chart) {
            this.chart.destroy();
            }
        });
    }

    drawChart() {
        debugger
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }

        const chartData = {
            labels: Object.keys(this.props.data),
            datasets: [{
                data: Object.values(this.props.data),
            }]
        };

        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: chartData,
            options: {
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const idx = elements[0].index;
                        const size = chartData.labels[idx];
                        this.openOrdersBySize(size);
                    }
                }
            }
        });
    }

    openOrdersBySize(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: `Orders with Size ${size.toUpperCase()}`,
            res_model: "sale.order",
            views: [[false, "list"]],
            domain: [["order_line.product_template_attribute_value_ids.display_name", "ilike", size]],
            context: {create: false}
        });
    }
}
