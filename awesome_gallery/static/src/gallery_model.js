import { KeepLast } from "@web/core/utils/concurrency";
import { useService } from "@web/core/utils/hooks";
import { url } from "@web/core/utils/urls";

export class GalleryModel {
    constructor(resModel, image_field, tooltip_field, limit) {
        this.orm = useService("orm");
        this.action = useService("action");
        this.keepLast = new KeepLast();

        this.resModel = resModel
        this.images = []
        this.imagesLength = 0
        this.image_field = image_field
        this.tooltip_field = tooltip_field
        this.limit = limit
        this.pager = { limit: limit, offset: 0 }
    }

    async loadImages(domain) {
        const specification = {
            [this.image_field]: {},
            [this.tooltip_field]: {},
        };
        const { length, records } = await this.keepLast.add(
            this.orm.webSearchRead(this.resModel, domain, {
                limit: this.pager.limit,
                offset: this.pager.offset,
                specification,
                context: {
                    bin_size: true,
                }
            })
        );
        records.forEach(element => {
            element.url = url(
                "/web/image",
                {
                    model: this.resModel,
                    id: element.id,
                    field: this.image_field,
                }
            )
        });
        this.images = records;
        this.imagesLength = length;
    }


}