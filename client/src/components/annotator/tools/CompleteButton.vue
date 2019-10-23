<script>
import button from "@/mixins/toolBar/button";

export default {
  name: "CompleteButton",
  mixins: [button],
  data() {
    return {
      name: "Complete",
      icon: "fa-check"
    };
  },
  methods: {
    execute() {
      this.$parent.updateStatus('completed');
    }
  }
};
</script>
