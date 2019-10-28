<template>
  <p class="text-center" v-if="images.length < 1">
    No images found.
  </p>
  <div v-else>
    <p class="text-center">
      Total of <strong>{{ total }}</strong> images
      displayed on <strong>{{ pages }}</strong> pages.
    </p>
    <Pagination :pages="pages" @pagechange="update" />
    <div class="row">
      <ImageCard v-for="image in images" :key="image.id" :image="image" />
    </div>
    <Pagination :pages="pages" @pagechange="update" />
  </div>
</template>

<script>
import ImageCard from "@/components/cards/ImageCard";
import Pagination from "@/components/Pagination";

export default {
  name: "ImagesList",
  components: {
    ImageCard,
    Pagination,
  },
  props: {
    images: {
      type: Array,
      required: true
    },
    pages: {
      type: Number,
      required: true
    },
    total: {
      type: Number
    },
    update: {}
  },
  data() {
    return {
      limit: 52,
      status: {
        data: { state: true, message: "Loading data" }
      },
    };
  },
}

</script>