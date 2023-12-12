import { defineStore } from "pinia";
import type { Article } from "@/types.ts";

export const useArticleStore = defineStore('article', {
    state: () => {
        return {
            articles: [] as Article[],
        }
    },
    actions: {
        async populate() {
            const response = await fetch('http://127.0.0.1:8000/api/articles/')
            if (response.ok) {
                this.articles = await response.json()
            }
        }
    }
})