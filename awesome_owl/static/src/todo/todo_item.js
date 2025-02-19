/** @odoo-module **/

import { Component,xml } from "@odoo/owl";

export class TodoItem extends Component{
    static props = {
            id:Number,
            description:String,
            isCompleted:Boolean
    }

   

    static template = xml`
        <div class="card d-inline-block p-2">
            <p><t t-out="props.id"/>.<t t-out="props.description"/></p>
        </div>
    `

    
}