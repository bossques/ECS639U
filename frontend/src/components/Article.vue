<template>
    <div v-if="article" class="card p-2">
        <div class="card-title row">
            <div class="">
                {{ article.title }} - {{ article.category.name }}
            </div>

            <div class="">
                {{ article.created_at }}
            </div>
        </div>
        <div class="card-body">
            {{ article }}
        </div>
    </div>
</template>

<script lang="ts">
import {Article} from "@/types.ts";

export default {
    props: {
        article: Object as () => Article
    }
}
</script>