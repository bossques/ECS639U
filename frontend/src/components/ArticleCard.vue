<template>
    <router-link
        v-if="article"
        :to="{name: 'Article Page', params: { id: article.id }}"
        class="text-decoration-none card p-2 hover-effect">
        <div class="card-body">
            <h4 class="card-title">
                {{ article.title }}
            </h4>

            <small class="card-subtitle">
                {{ formatDate(article.created_at) }}
            </small>
        </div>
    </router-link>
</template>

<script lang="ts">
import { Article } from "@/types.ts";

export default {
    props: {
        article: Object as () => Article
    },
    methods: {
        formatDate(datetimeString: string) {
            const datetime = new Date(datetimeString)
            const options: Intl.DateTimeFormatOptions = {year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'}

            return datetime.toLocaleString('en-US', options)
        }
    }
}
</script>

<style scoped>
.hover-effect {
  transition: transform 0.3s ease;
}

.hover-effect:hover {
  transform: scale(1.03);
}
</style>