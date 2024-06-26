/** @odoo-module */

import { registry } from "@web/core/registry";
import { GalleryController } from "./controller/gallery_controller";
import { GalleryXmlArchParser } from "./gallery_arch_parser";
import { GalleryRenderer } from "./renderer/gallery_renderer";
import { GalleryModel } from "./gallery_model";

export const galleryView = {
    type: "gallery",
    display_name: "Gallery",
    icon: "fa fa-picture-o",
    multiRecord: true,
    Controller: GalleryController,
    Renderer: GalleryRenderer,
    Model: GalleryModel,
    ArchParser: GalleryXmlArchParser,
    props: (genericProps, view) => {
        const { arch, relatedModels, resModel } = genericProps;
        const archInfo = new view.ArchParser().parse(arch, relatedModels, resModel);
        return {
            ...genericProps,
            archInfo,
            Model: view.Model,
            Renderer: view.Renderer,
        };
    },
};

registry.category("views").add("gallery", galleryView);
