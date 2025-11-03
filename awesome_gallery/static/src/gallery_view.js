/** @odoo-module */

import { registry } from "@web/core/registry";
import { GalleryController } from "./gallery_controller";
import { galleryArchParser } from "./gallery_arch_parser";
import {GalleryModel} from "./gallery_model";
import {GalleryRenderer} from "./gallery_renderer";

export const galleryView = {
      type: "gallery",
      display_name: "Gallery",
      icon: "fa fa-picture-o",
      multiRecord: true,
      Controller: GalleryController,
      ArchParser: galleryArchParser,
      Model: GalleryModel,
      Renderer: GalleryRenderer,

      props(genericProps, view) {
        const { arch } = genericProps;
        const parser = new view.ArchParser();
        const archInfo = parser.parse(arch);
        const gallerymodel = view.Model;
        const galleryrenderer = view.Renderer;

        return {
            ...genericProps,
            archInfo,
            Model: gallerymodel,
            Renderer: galleryrenderer
        };
    },
};

registry.category("views").add("gallery", galleryView);
