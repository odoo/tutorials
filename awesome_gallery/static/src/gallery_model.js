export class GalleryModel {
    constructor(orm, resModel, archInfo) {
        this.orm = orm;
        this.resModel = resModel;
        this.records = [];

        const { imageField, limit, tooltipField } = archInfo;
        this.imageField = imageField;
        this.limit = limit;
        this.tooltipField = tooltipField;
    }

    async load(domain) {
        const { records } = await this.orm.webSearchRead(
            this.resModel,
            domain,
            {
                limit: this.limit,
                specification: {
                    [this.imageField]: {},
                    ["name"]: {},
                },
                context: {
                    bin_size: true,
                }
            }
        );
        this.records = records;
    }
}
