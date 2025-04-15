<template>
  <main class="container text-white">
    <div class="pt-4 mb-8 relative">
      <input 
        type="text"
        v-model="searchQuery"
        @input="getSearchResults"
        placeholder="Search for a city or state" 
        class="py-2 px-1 w-full bg-transparent border-b 
        focus:border-weather-secondary focus:outline-none 
        focus:shadow-[0px_1px_0_0_#004E71]">
        <ul class="absolute bg-weather-secondary text-white w-full shadow-md py-2 px-1 top-[66px]" v-if="mapboxSearchResults">
          <p v-if="searchError">Sorry, something went wrong, please try again.</p>
          <p v-if="!serverError && mapboxSearchResults.length === 0">No results match your query, try a different term.</p>
          <template v-else>
            <li v-for="searchResult in mapboxSearchResults" :key="searchResult.id" class="py-2 cursor-pointer" @click="previewCity(searchResult)">
              {{ searchResult.properties.full_address }}
            </li>
          </template>
        </ul>
    </div>
    <div class="flex flex-col gap-4">
      <Suspense>
        <CityList />
        <template #fallback>
          <CityCardSkeleton />
        </template>
      </Suspense>
    </div>
  </main>
</template>

<script setup>
import {ref} from "vue"; 
import axios from "axios";
import {useRouter} from "vue-router";
import CityList from "../components/CityList.vue";
import CityCardSkeleton from "../components/CityCardSkeleton.vue";

const router = useRouter();
const previewCity = (searchResult) => {
  const [city, state] = searchResult.properties.full_address.split(",");
  router.push({
    name: "cityView",
    params: { state: state.replaceAll(" ", ""), city: city },
    query: {
      lat: searchResult.properties.coordinates.latitude,
      lng: searchResult.properties.coordinates.longitude,
      preview: true
    }
  })
}

const mapboxApiKey = "pk.eyJ1IjoibmNoYW43IiwiYSI6ImNtMHZncXVuZjA5MmgycW9kOW01a296NHMifQ.zJZY32kDnJklDriiOIorwQ"
const searchQuery = ref("");
const queryTimeout = ref(null);
const mapboxSearchResults = ref(null);
const searchError = ref(null);

const getSearchResults = () => {
  clearTimeout(queryTimeout.value)
  queryTimeout.value = setTimeout(async () => {
    if (searchQuery.value !== "") {
      try {
        const result = await axios.get(`https://api.mapbox.com/search/geocode/v6/forward?q=${searchQuery.value}&types=place&access_token=${mapboxApiKey}`);
        mapboxSearchResults.value = result.data.features;
      } catch {
        searchError.value = true
      }
      return;
    }
    mapboxSearchResults.value = null
  }, 300);
}
</script>

