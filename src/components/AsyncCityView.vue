<template>
    <div class="flex flex-col flex-1 items-center">
        <!-- Banner -->
        <div v-if="route.query.preview" class="text-white p-4 bg-weather-secondary w-full text-center">
            <p>You are currently previewing this city, click the "+" icon to start tracking this city.</p>
        </div>

        <!--New Design-->
        <div class="flex flex-col my-10 p-8 rounded-md w-9/12 sm:px-12 dark:bg-weather-secondary dark:text-white">
            <div class="items-center text-center">
                <h2 class="text-xl font-semibold">{{ route.params.city }}</h2>
                <p class="text-sm dark:text-white">
                    {{ new Date().toLocaleDateString("en-us",
                    {
                        weekday: "short",
                        day: "2-digit",
                        month: "long",
                        year: "numeric"
                    }) 
                }}
            
                {{ new Date().toLocaleTimeString("en-us",
                    {
                        timeStyle: "short",
                    }) 
                }}
                </p>
                <p class="text-8xl mb-8">
                    {{ Math.round((currentWeatherData.main.temp - 32) * 5/9) }}&deg;
                </p>
                            <p>{{ Math.round((currentWeatherData.main.temp_max - 32) * 5/9) }}&deg; / {{ Math.round((currentWeatherData.main.temp_min - 32) * 5/9) }}&deg;</p>
            <p class="capitalize">
                {{ currentWeatherData.weather[0].description }}
            </p>
            <!-- <img
                class="mx-auto"
                :src="
                `http://openweathermap.org/img/wn/${currentWeatherData.weather[0].icon}@2x.png`
                "
                alt=""
            /> -->
            </div>
        </div>
        <!--New Design End-->
        <!-- Weather Overview -->
        <div class="w-full sm:px-12">
            <div class="gap-4 mx-2 text-white pb-4 grid grid-cols-3 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-3">
                <div class="text-center  dark:bg-weather-secondary dark:text-white rounded-md p-8">
                    <i class="fa-solid fa-wind mb text-2xl"></i>
                    <p class="text-lg md:text-xl font-bold">
                        {{ `${currentWeatherData.wind.speed} km/h` }}
                    </p>
                    <p>Wind</p>
                </div>
                <div class="text-center dark:bg-weather-secondary dark:text-white rounded-md p-8">
                    <i class="fa-solid fa-droplet mb text-2xl"></i>
                    <p class="text-lg md:text-xl font-bold">
                        {{ `${currentWeatherData.main.humidity}%` }}
                    </p>
                    <p>Humidity</p>
                </div>
                <div class="text-center  dark:bg-weather-secondary dark:text-white rounded-md p-8">
                    <i class="fa-solid fa-umbrella mb text-2xl"></i>
                    <p class="text-lg md:text-xl font-bold">
                        {{ currentWeatherData.rain ? `${currentWeatherData.rain['1h']}%` : `${0}%` }}
                    </p>
                    <p>Precipitation</p>
                </div>
                <div class="text-center dark:bg-weather-secondary dark:text-white rounded-md p-8">
                    <i class="fa-solid fa-fan mb text-2xl"></i>
                    <p class="text-lg md:text-xl font-bold">
                        {{ `${currentWeatherData.wind.direction}` }}
                    </p>
                    <p>Direction</p>
                </div>
                <div class="text-center dark:bg-weather-secondary dark:text-white rounded-md p-8">
                    <i class="fa-solid fa-temperature-half mb text-2xl"></i>
                    <p class="text-lg md:text-xl font-bold">
                        {{ `${Math.round((currentWeatherData.main.feels_like - 32) * 5/9)}&deg;` }}
                    </p>
                    <p>Feels</p>
                </div>
                <div class="text-center dark:bg-weather-secondary dark:text-white rounded-md p-8">
                    <i class="fa-solid fa-sun mb text-2xl"></i>
                    <p class="text-lg md:text-xl font-bold">
                        {{ `${currentWeatherData.main.humidity}%` }}
                    </p>
                    <p>UV Index</p>
                </div>
            </div>
        </div>

        <hr class="border-white border-opacity-10 border w-full" />

        <!-- Weekly Weather -->
        <div class="max-w-screen-md w-full py-12">
            <h2 class="mb-4 text-white">5 Days Forecast</h2>
            <div class="gap-4 mx-2 text-white pb-4 grid grid-cols-5 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-5">
                <div 
                v-for="(day,index) in fiveDayForecastWeatherData.list"
                :key="index" :class="{'remove-div': (index+1) % 8 != 0}" >
                    <div class="text-center dark:bg-weather-secondary dark:text-white rounded-md p-4">
                            <p class="flex-1">
                            {{
                            new Date(day.dt * 1000).toLocaleDateString(
                                "en-us",
                                {
                                weekday: "long",
                                }
                            )
                            }}
                            </p>
                            <img
                                class="mx-auto w-[50px] h-[50px] object-cover"
                                :src="
                                `http://openweathermap.org/img/wn/${day.weather[0].icon}@2x.png`
                                "
                                alt=""
                            />
                            <div class="temp">
                                <p>Highest: {{ Math.round((day.main.temp_max - 32) * 5/9) }}</p>
                                <p>Lowest: {{ Math.round((day.main.temp_min - 32) * 5/9) }}</p>
                            </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="flex items-center gap-2 py-12 text-white cursor-pointer duration-150 hover:text-red-500" @click="removeCity">
            <i class="fa-solid fa-trash"></i>
            <p>Remove City</p>
        </div>
    </div>
</template>

<script setup>
import axios from "axios";
import {useRoute, useRouter} from "vue-router";

const route = useRoute();
const getCurrentWeatherData = async () => {
    try {
        const currentWeatherData = await axios.get(
            `https://api.openweathermap.org/data/2.5/weather?lat=${route.query.lat}&lon=${route.query.lng}&appid=603a1664ad6df64bf1a0df46762d9edc&units=imperial`);
        // calculate current date & time
        const localOffset = new Date().getTimezoneOffset() * 60000;
        const utc = currentWeatherData.data.dt * 1000 + localOffset;
        currentWeatherData.data.currentTime =
        utc + 1000 * currentWeatherData.data.timezone;

        //calculate wind direction
        let degrees = currentWeatherData.data.wind.deg;
        let directions = ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest'];
        degrees = degrees * 8 / 360;
        // round to nearest integer.
        degrees = Math.round(degrees, 0);
        // Ensure it's within 0-7
        degrees = (degrees + 8) % 8
        currentWeatherData.data.wind.direction = directions[degrees]

        //Flicker delay
        await new Promise((res) => setTimeout(res, 1000));

        return currentWeatherData.data;
    } catch (error) {
        console.log(error)
    }
}

const getFiveDayForecastWeatherData = async () => {
    try {
        const fiveDayForecastWeatherData = await axios.get(
            `https://api.openweathermap.org/data/2.5/forecast?lat=${route.query.lat}&lon=${route.query.lng}&appid=603a1664ad6df64bf1a0df46762d9edc&units=imperial`);
        //Flicker delay
        await new Promise((res) => setTimeout(res, 1000));
        //Day Display
        return fiveDayForecastWeatherData.data;
    } catch (error) {
        console.log(error)
    }
}

const currentWeatherData = await getCurrentWeatherData();
const fiveDayForecastWeatherData = await getFiveDayForecastWeatherData();

const router = useRouter();
const removeCity = () => {
    const cities = JSON.parse(localStorage.getItem("savedCities"));
    const updatedCities = cities.filter((city) => city.id !== route.query.id);
    localStorage.setItem("savedCities", JSON.stringify(updatedCities));
    router.push({
        name: "home",
    }) 
}
</script>
<style scoped>
.remove-div{display: none;}
</style>