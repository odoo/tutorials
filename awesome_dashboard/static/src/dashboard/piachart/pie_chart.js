import { Component, onWillStart, onMounted, useRef, onWillUpdateProps,useState } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvas");
        this.action = useService("action");
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        this.chart = null;
        
        onMounted(() => {
            if(!this.chart)
                this.renderChart();
        });
        onWillUpdateProps(() => {
            this.renderChart();
        });
    }

    renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");
        const data = this.props.data || {};
        const labels = Object.keys(data); 

        if (this.chart) {
            this.chart.data.labels = Object.keys(data);
            this.chart.data.datasets[0].data = Object.values(data);
            this.chart.update();
        } 
        else {
            this.chart = new Chart(ctx, {
                type: "pie",
                data: {
                    labels: labels,
                    datasets: [{
                        data: Object.values(data),
                    }],
                },
                options: {
                    onClick: (evt, elements) => {
                        if (elements.length > 0) {
                            const index = elements[0].index;

                            const selectedSize = labels[index];

                            this.openOrders(selectedSize);
                        }
                    },
                },
            });
        }
    }
    openOrders(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Orders",
            res_model: "sale.order",
            views: [
                [false, "list"],
                [false, "form"]
            ],
            domain: [["order_line.product_id.product_template_attribute_value_ids.product_attribute_value_id.name", "=", size]],  // 👈 IMPORTANT
            target: "current",
        });
    }

}
