import { Component, computed, signal } from "@odoo/owl";
import { Counter } from "./counter";
import { ProductCard } from "./product_card";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, ProductCard };

  headphone = {
    name: "Wireless Headphones",
    description: "Noise-cancelling over-ear headphones",
    price: 79.99,
    image: "🎧",
  };
  keyboard = {
    name: "Mechanical Keyboard",
    description: "RGB backlit mechanical keyboard",
    price: 129.99,
    image: "⌨️",
  };
  webcam = {
    name: "Webcam HD",
    description: "1080p webcam with microphone",
    price: 59.99,
  };

  name = signal("");
  email = signal("");
  greeting = computed(() => `Hello ${this.name()}`);
  isValid = computed(() => this.name().length > 0 && this.email().length > 0 && this.email().includes("@"));
}
