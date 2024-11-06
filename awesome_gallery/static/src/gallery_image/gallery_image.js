/** @odoo-module */

const {Component} = owl;

export class GalleryImage extends Component {
    static template = "awesome_gallery.GalleryImage";
    static props = {
        image: Object,
        imageField: String,
        tooltipField: String,
        className: String,
        onClick: Function
    };


    onClick() {
        this.props.onClick(this.props.image.id);
    }
}
