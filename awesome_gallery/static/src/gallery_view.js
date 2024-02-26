/** @odoo-module */

import { registry } from "@web/core/registry";
import { GalleryController } from "./gallery_controller";
import { GalleryArchParser } from "./gallery_arch_parser";
import { GalleryModel } from "./gallery_model";
import { GalleryRenderer } from "./gallery_renderer";

export const galleryView = {
      type: "gallery",
      display_name: "Gallery",
      icon: "fa fa-picture-o",
      multiRecord: true,
      Controller: GalleryController,
      ArchParser: GalleryArchParser,

      props(genericProps, view) {
            const {ArchParser} = view;
            const {arch} = genericProps;
            const archInfo = new ArchParser().parse(arch);

            return {
                  ...genericProps,
                  archInfo,
                  Model: GalleryModel,
                  Renderer: GalleryRenderer
            }
      }
};

registry.category("views").add("gallery", galleryView);
