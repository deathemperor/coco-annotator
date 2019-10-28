<template>
  <div>
    <div style="padding-top: 55px" />
    
    <div
      class="bg-light"
    >
      <div class="bg-light text-left" style="overflow: auto; height: calc(100vh - 100px); margin: 10px">
        <div class="container">
          
          <div style="padding-top: 10px" />
          <h3 class="text-center">
            <i
              class="fa fa-circle color-icon"
              aria-hidden="true"
              :style="{ color: category.color }"
            />
            {{ category.name }}
          </h3>
          <ImageList :images="images" :pages="pages" :update="updatePage" />

        </div>

      </div>
    </div>

  </div>
</template>

<script>
import toastrs from "@/mixins/toastrs";
import Dataset from "@/models/datasets";
import Category from "@/models/categories";
import ImageList from "@/components/ImageList";
import JQuery from "jquery";

import { mapMutations } from "vuex";

let $ = JQuery;

export default {
  name: "Dataset",
  components: {
    ImageList,
  },
  mixins: [toastrs],
  props: {
    categoryId: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      pages: 1,
      limit: 52,
      category: {},
      imageCount: 0,
      images: [],
      status: {
        data: { state: true, message: "Loading data" }
      },
    };
  },
  methods: {
    ...mapMutations(["addProcess", "removeProcess"]),
    updatePage(page) {
      let process = "Loading images from dataset";
      this.addProcess(process);

      Category.getImages(this.categoryId, {
        page: page,
        limit: this.limit,
        order: this.order
      })
        .then(response => {
          const { data } = response;

          this.category = data.category;
          this.images = data.images;
          this.imageCount = data.pagination.total;
          this.pages = data.pagination.pages;

        })
        .catch(error => {
          this.axiosReqestError("Loading Dataset", error.response.data.message);
        })
        .finally(() => this.removeProcess(process));
    },
  },
  computed: {
  },
  sockets: {
  },
  watch: {
  },
  created() {
    this.updatePage();
  },
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
