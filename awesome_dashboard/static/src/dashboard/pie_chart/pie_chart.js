import { Component, onWillStart,useRef, onMounted, onWillUnmount, useEnv } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { _t } from "@web/core/l10n/translation";



export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: {
            type: String,
            optional: true,
        },
        data: Object,
        clickview: {
            type: Function,
            optional: true,
        },
    }
    setup() {
        this.canvasRef = useRef("canvas_pie");
        this.env = useEnv();
        onWillStart(async () => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(()=> {
            this.renderChart();
        });  
            
        onWillUnmount(()=> {
            this.chart?.destroy();
        });

    }

  

    renderChart() {
        this.chart = new Chart(this.canvasRef.el,{
            type: 'pie',
            data : {
                labels : Object.keys(this.props.data),
                datasets:[
                    {
                    label: this.props.label,
                    data : Object.values(this.props.data),
                    },
                ],
            },
            options:{
                events: ['click'],
                onClick: (ev, section) => {
                    console.log(section);
                    const index = section[0].index
                    console.log("heere maybee ?");
                    const size = Object.keys(this.props.data)[index];
                    this.env.services.action.doAction({
                        type:'ir.actions.act_window',
                        name: _t("Orders - Size " + size),
                        target: 'current',
                        res_model: 'sale.order',
                        views: [[false,'list']],
                        domain: [['order_line.name', 'ilike', size]],
                    
                })

            }
            },
        });

    }
}

