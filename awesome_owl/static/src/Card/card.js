import { Component} from '@odoo/owl'


export class Card extends Component {
    static template = "awesome_owl.card"
    static prop = {
        title : {
            type: String
        },
        content: {
            type: String
        }
    }
}
