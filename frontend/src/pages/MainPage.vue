<template>
    <div v-for="(articles, category) in sortedArticles">
        <h3 class="p-2">{{ category }}</h3>

        <div class="row col-sm-12">
            <div v-for="article in articles" class="col-sm-3">
                <ArticleCard :article="article" />
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useArticleStore } from "@/store/articles.ts";
import { Article } from "@/types.ts";
import ArticleCard from "@/components/ArticleCard.vue";

export default defineComponent({
    components: {
        ArticleCard
    },
    computed: {
        sortedArticles(): Record<string, Article[]> {
            return useArticleStore().articles.reduce((result, article) => {
                const categoryName = article.category.name
                result[categoryName] = [...(result[categoryName] || []), article]
                return result
            }, {} as Record<string, Article[]>)
        }
    }
})

</script>

<style scoped>
</style>
