<template>
    <div class="card py-2">
        <h2>All News</h2>
    </div>

    <div v-for="(articles, category) in sortedArticles" class="py-3" :key="category">
        <h3>{{ category }}</h3>

        <div class="row col-sm-12">
            <div v-for="article in articles" class="col-sm-3" :key="article.id">
                <ArticleCard :article="article" />
            </div>
        </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";
import { useArticleStore } from "@/store/articleStore.ts";
import { Article } from "@/types.ts";
import ArticleCard from "@/components/ArticleCard.vue";

export default defineComponent({
    components: {
        ArticleCard
    },
    computed: {
        sortedArticles(): Record<string, Article[]> {
            let articles = useArticleStore().articles

            // sort by categories
            return articles.reduce((result, article) => {
                const categoryName = article.category.name
                result[categoryName] = [...(result[categoryName] || []), article]
                return result
            }, {} as Record<string, Article[]>)
        }
    }
})

</script>
  