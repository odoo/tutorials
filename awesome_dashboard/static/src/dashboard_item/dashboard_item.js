import { Component } from "@odoo/owl"

export class DashBoardItem extends Component{
    static template = "awesome_owl.dashboardItem"
    static props = {
        slots:{
            "type": Object,
            "shape":{
                default: Object
            }
        },
        size:{
            type:Number,
            optional: true
        }
    }
    static defaultProps ={
        size: 1
    }

}
