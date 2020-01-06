<template>
  <div>
    <div style="padding-top: 55px" />

    <div class="bg-light">
      <div
        class="bg-light text-left"
        style="overflow: auto; height: calc(100vh - 100px); margin: 10px"
      >
        <div class="container">
          Filter: <select v-model="status">
                    <option>completed</option>
                    <option>verified</option>
                    <option>rejected</option>
                  </select>
          <div style="padding-top: 10px" />
          <ImageList
            :images="images"
            :pages="pages"
            :update="updatePage"
            :total="imageCount"
          />

        </div>

      </div>
    </div>

  </div>
</template>

<script>
import toastrs from "@/mixins/toastrs";
import User from "@/models/user";
import ImageList from "@/components/ImageList";
import JQuery from "jquery";

import { mapMutations } from "vuex";

let $ = JQuery;

export default {
  name: "Dataset",
  components: {
    ImageList
  },
  mixins: [toastrs],
  props: {
    username: {
      type: String,
      required: true
    },
    date: {
      type: String
    }
  },
  data() {
    return {
      pages: 1,
      imageCount: 0,
      images: [],
      status: ""
    };
  },
  methods: {
    ...mapMutations(["addProcess", "removeProcess"]),
    updatePage(page) {
      let process = "Loading images";
      this.addProcess(process);

      User.getUserImages(this.username, {
        date: this.date,
        page: page,
        limit: this.limit,
        status: this.status
      })
        .then(response => {
          const { data } = response;

          this.images = data.images;
          this.imageCount = data.pagination.total;
          this.pages = data.pagination.pages;
        })
        .catch(error => {
          this.axiosReqestError("Loading Images", error.response.data.message);
        })
        .finally(() => this.removeProcess(process));
    }
  },
  computed: {},
  sockets: {},
  watch: {
    status() {
      this.$router.replace({query: {...this.$route.query, status: this.status}})
    }
  },
  created() {
    if (!this.$store.getters['user/isAdmin'] || !this.$store.getters['user/user'] 
        || this.$store.getters['user/user'].username !== this.username) {
      return;
    }
    this.status = this.$route.query.status;
    this.updatePage();
  }
};
</script>

<style scoped>
.breadcrumb {
  padding: 0px;
  margin: 5px 0;
}

.btn-link {
  padding: 0px;
}

.sidebar .title {
  color: white;
}

.progress {
  padding: 2px;
  height: 24px;
}

.sidebar {
  height: 100%;
  position: fixed;
  color: white;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: #4b5162;
  overflow-x: hidden;
  padding-top: 60px;
}

.sidebar .closebtn {
  position: absolute;
  top: 0;
  right: 25px;
  font-size: 36px;
  margin-left: 50px;
}

.sidebar-title {
  color: white;
}

.sidebar-section-buttons {
  margin: 5px;
}

.sidebar-section {
  margin: 5px;
  border-radius: 5px;
  background-color: #383c4a;
  padding: 0 5px 2px 5px;
  overflow: auto;
}
</style>
