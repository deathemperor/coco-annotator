<script>
import button from "@/mixins/toolBar/button";

export default {
  name: "RejectButton",
  mixins: [button],
  data() {
    return {
      name: "Reject",
      icon: "fa-times"
    };
  },
  methods: {
    execute() {
      this.$parent.updateStatus("rejected");
    }
  }
};
</script>
