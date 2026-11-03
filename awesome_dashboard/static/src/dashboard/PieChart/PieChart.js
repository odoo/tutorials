import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useRef,onMounted,onPatched,onWillUnmount} from "@odoo/owl";

export class PieChart extends Component 
{
    static template = "awesome_dashboard.PieChart"
    static props = {
        label : String,
        data : {type : Object, optional: true},
    }
    setup()
    {
        this.canvasRef = useRef("canvas");
        this.action = useService("action");
        onWillStart(()=> loadJS("/web/static/lib/Chart/Chart.js"))

        onMounted(()=> {this.renderChart();});

        onPatched(() =>{
            this.chart.destroy();
            this.renderChart();
        });

        onWillUnmount(()=> {this.chart.destroy();});
    }

    renderChart()
    {
        this.chart = new Chart(this.canvasRef.el,
            {
                type: 'doughnut',
                data:{
                    labels:Object.keys(this.props.data),
                    datasets: [
                        {
                            data: Object.values(this.props.data),
                            label: this.props.label
                        }
                    ]
                },
                options: {
                    responsive: true,
                    onClick: (e) =>{
                        const activePoints = this.chart.getElementsAtEventForMode(e, 'nearest', {
                        intersect: true
                    }, false);
                    if (activePoints.length > 0) {
                        const index = activePoints[0].index;
                        const label = this.chart.data.labels[index];
                        const value = this.chart.data.datasets[0].data[index];
                        this.onClick(label)
                    }
                    }
                    // events: ['click'],
                },
                // plugins: [{
                //     id: 'custome_plugin',
                //     afterEvent(chart, args, pluginOptions)
                //     { 
                //         // this.onClick(chart.tooltip.title)
                //         console.log(args);
                //         import { useService } from "@web/core/utils/hooks";
                //         this.action = useService("action");
                //         // this.action.doAction(({
                //         //     type: 'ir.actions.act_window',
                //         //     name: "All leads",
                //         //     res_model: 'account.move',
                //         //     views: [[0,'list'],[1,'form']]
                //         // }));
                //     }
                // }]

            });

    }
    onClick(title)
    {
        this.action.doAction(({
            type: 'ir.actions.act_window',
            name: "Sales Order",
            res_model: 'sale.order',
            //domain: [["order_line.product_id.name", "=", "Shirt"]],
            domain: [["order_line.product_id.product_template_variant_value_ids.product_attribute_value_id.display_name", "=", title]],
            views: [[0,'list'],[1,'form']]
        }));
    }

}
