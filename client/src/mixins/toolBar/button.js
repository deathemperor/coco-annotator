export default {
  template:
    "<div :style='{fontSize: fontSize}'><i v-tooltip.right='name' class='fa fa-x' :class='icon' :style='{ color: iconColor }' @click='click'></i><br></div>",
  data() {
    return {
      color: {
        enabled: "white",
        active: "#2ecc71",
        disabled: "gray"
      },
      iconColor: "",
      delay: 400
    };
  },
  props: {
    activeColor: {
      type: String
    },
    fontSize: {
      type: String,
      default: "1.0rem"
    }
  },
  methods: {
    click() {
      if (!this.disabled) {
        this.toggleAnimation();
        this.execute();
      }
    },
    toggleAnimation() {
      this.iconColor = this.color.active;
      setTimeout(() => {
        this.iconColor = this.color.enabled;
      }, this.delay);
    }
  },
  watch: {
    activeColor() {
      if (this.activeColor) {
        this.iconColor = this.activeColor;
      }
    }
  },
  created() {
    if (this.activeColor) {
      this.iconColor = this.activeColor;
    } else {
      this.iconColor = this.color.enabled;
    }
  }
};
