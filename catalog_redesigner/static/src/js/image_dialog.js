import { Component } from "@odoo/owl"

export class ImageDialog extends Component {
    static template = "product_view_kanban_catalog_inherit.image_dialog"
    static props = {
        imgSrc: String,
        close: Function,
    }
}
