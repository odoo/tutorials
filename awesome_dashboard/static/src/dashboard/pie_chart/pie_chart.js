    import { loadJS } from "@web/core/assets";
    import { getColor } from "@web/core/colors/colors";
    import { Component, onWillStart , useRef , onMounted , onWillUnmount} from "@odoo/owl";
    import { useService } from "@web/core/utils/hooks";

    export class PieChart extends Component{
        static template = "awesome_dashboard.PieChart";
        static props = {
            label: String,
            data: Object,
        };

        setup(){
            this.canvasRef = useRef("canvas");
             this.actionService = useService("action");
            onWillStart(()=>loadJS("/web/static/lib/Chart/Chart.js"));
            onMounted(() => {
                this.renderChart();
            });
            onWillUnmount(() => {
                if(this.chart){
                    this.chart.destroy();
                }
            });
        }

        renderChart(){
            const labels = Object.keys(this.props.data);
            const data = Object.values(this.props.data);
            const color = labels.map((_, index) => getColor(index));
            this.chart = new Chart(this.canvasRef.el, {
                type: "pie",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: this.props.label,
                            data: data,
                            backgroundColor: color,
                        },
                    ],
                },
                options: {
                    onClick: (event, elements) => {
                        if (elements.length > 0) {
                            const index = elements[0].index;
                            const size = labels[index];
                            this.openOrdersBySize(size);
                        }
                    },
                },
            });
        }

        openOrdersBySize(size) {
            this.actionService.doAction({
                type: "ir.actions.act_window",
                name: `Orders - Size ${size}`,
                res_model: "sale.order", //just to demonstrate 
                views: [[false, "list"]],
                domain: [["id", "=", -1]], // always empty (demo only)
            });
        }
    }