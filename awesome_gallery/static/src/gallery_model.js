export class GalleryModel {
    constructor(orm, resModel, archInfo) {
        this.orm = orm;
        this.resModel = resModel;
        this.records = [];

        const { imageField, limit, tooltipField } = archInfo;
        this.imageField = imageField;
        this.limit = limit;
        this.tooltipField = tooltipField;

        this.pager = { offset: 0, limit: limit };
    }

    async load(domain) {
        const { length, records } = await this.orm.webSearchRead(
            this.resModel,
            domain,
            {
                limit: this.pager.limit,
                offset: this.pager.offset,
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
        this.recordsLength = length;
    }
}
