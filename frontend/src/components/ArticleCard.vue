<template>
    <div v-if="article" class="card p-2 hover-effect">
        <div class="card-body">
            <h4>
                {{ article.title }}
            </h4>

            <small class="grey">
                {{ formatDate(article.created_at) }}
            </small>
        </div>
    </div>
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
  transform: scale(1.01);
}
</style>