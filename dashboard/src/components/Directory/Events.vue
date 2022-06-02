<template>
  <v-container>
    <v-row dense>
      <v-col
        v-for="(item, i) in items"
        :key="i"
        cols="12"
        xs="12"
        sm="12"
        lg="6"
        xl="6"
      >
        <v-card>
          <div class="d-flex flex-no-wrap justify-space-between">
            <div>
              <v-card-title class="text-b" v-text="item.name"></v-card-title>
              <v-card-subtitle>{{ formatDateAndTime(item.datestart) }}</v-card-subtitle>
            </div>

            <v-avatar class="ma-3" size="80" tile>
              <template
                v-if="item.images !== undefined && item.images.length > 0"
              >
                <v-img :src="item.images[0]"></v-img>
              </template>
              <template v-else>
                <v-icon class="icon-not-found-image">mdi-calendar</v-icon>
              </template>
            </v-avatar>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-card
      v-show="renderFinished && !isLoading"
      v-intersect="infiniteScrolling"
    ></v-card>
  </v-container>
</template>

<script>
import { getJSON } from "@/helpers/Request";
import { notification } from "@/helpers/Notifications";
import { formatDateAndTime } from "@/helpers/Date"

export default {
  name: "Events",
  data() {
    return {
      items:  [],
      start_key: "",
      renderFinished: false,
      isLoading: false,
      isTheLast: false,
    };
  },
  updated() {
    this.renderFinished = true;
  },
  created() {
    this.getEvents();
  },
  methods: {
    formatDateAndTime,
    infiniteScrolling() {
      if (this.isTheLast || this.isLoading || !this.renderFinished) {
        return;
      }

      this.isLoading = true;
      setTimeout(() => {
        this.getEvents();
      }, 500);
    },
    getEvents() {
      this.isLoading = true;
      getJSON(
        "/events",
        {
          start_key: this.start_key,
        },
        false
      )
        .then((res) => {
          if (res.error) {
            notification({
              message: res.message,
            });

            return;
          }

          this.renderFinished = false;
          this.items.push(...res.data.items);

          if (res.data.start_key !== undefined) {
            this.start_key = res.data.start_key;
          } else {
            this.isTheLast = true;
          }

          this.isLoading = false;
        })
        .catch(() => {
          this.isLoading = false;
          notification({
            message: "Ocurrió un error al hacer la petición",
          });
        });
    },
  },
};
</script>

<style scoped>
.theme--light.v-card {
  background-color: #f5f5f5;
}

.event-container {
  width: 100%;
  height: 100vh;
}

.icon-not-found-image{
  font-size: 40px !important;
}
</style>
