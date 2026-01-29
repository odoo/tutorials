import { Component, onWillStart, onWillUpdateProps, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { KeepLast } from "@web/core/utils/concurrency";
import { ImageBox } from "./image_box/image_box";

export class GalleryController extends Component {
    static template = "awesome_gallery.GalleryView"

    static components = {
        Layout,
        ImageBox
    }

    setup() {
        this.orm = useService("orm");
        this.data = useState({records: []})
        this.keepLast = new KeepLast();

        onWillStart(() => {
            this.loadImages([]);
        })

        onWillUpdateProps(() => {
            this.loadImages([]);
        })
    }

    async loadImages(domain) {
        const result = await this.keepLast.add(this.orm.webSearchRead("res.partner", domain, {
            specification : {
                id: {},
            },
            context: {
                bin_size: true,
            }
        }))

        this.data.records = result.records;
        
        console.log(this.data);
    }
}

export class GalleryArchParser {
    parse(xmlDoc) {
        debugger;
        const imageField = xmlDoc.getAttribute("image_field");
        return {
            imageField
        }
    }
}
