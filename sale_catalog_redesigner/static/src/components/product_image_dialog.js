import { Component, useState } from "@odoo/owl";

export class ImageDialog extends Component {
    static template = "product_view_kanban_catalog_inherit.image_dialog";
    static props = {
        imgSrc: String,
        productName: String,
        close: Function,
    };

    setup() {
        this.state = useState({
            zoomScale: 1.0,
        });
    }

    zoomIn() {
        if (this.state.zoomScale < 3.0) {
            this.state.zoomScale += 0.25;
        }
    }

    zoomOut() {
        if (this.state.zoomScale > 0.5) {
            this.state.zoomScale -= 0.25;
        }
    }

    resetZoom() {
        this.state.zoomScale = 1.0;
    }

    async downloadImage() {
        try {
            const response = await fetch(this.props.imgSrc);
            const blob = await response.blob();
            const blobUrl = window.URL.createObjectURL(blob);

            const link = document.createElement("a");
            link.href = blobUrl;

            const safeName = this.props.productName.replace(/[^a-z0-9]/gi, '_').toLowerCase();
            link.download = `${safeName}_product_image.png`;

            document.body.appendChild(link);
            link.click();

            document.body.removeChild(link);
            window.URL.revokeObjectURL(blobUrl);
        } catch (error) {
            console.error("Download execution interrupted:", error);
            window.open(this.props.imgSrc, '_blank');
        }
    }
}
