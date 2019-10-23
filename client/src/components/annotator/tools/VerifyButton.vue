<script>
import button from "@/mixins/toolBar/button";

export default {
  name: "VerifyButton",
  mixins: [button],
  data() {
    return {
      name: "Verify",
      icon: "fa-check-circle"
    };
  },
  methods: {
    execute() {
      this.$parent.updateStatus('verified');
    }
  }
};
</script>
