<template>
    <div v-if="article !== undefined">
        <h4>{{ article.title }}</h4>
        <p>{{ article.contents }}</p>
    </div>

    <div class="py-2 d-flex align-items-center flex-row">
        <h5>{{ comments.length }} Comments</h5>
        <input
            type="button"
            class="btn btn-secondary ms-auto"
            data-bs-toggle="modal"
            data-bs-target="#createCommentModal"
            value="Comment"
            ref="createCommentModal"
            v-if="loggedIn" />
    </div>

    <div v-for="comment in viewableComments" v-if="!isLoading" :key="comment.id">
        <CommentCard :comment="comment" @delete="deleteComment" @edit="onEdit" @reply="onReply" />
    </div>
    <div v-else>
        <p>Loading...</p>
    </div>

    <CommentCreateModal :reply_to="reply_to" @create-comment="createComment" @close="reply_to = null" id="createCommentModal"/>
    <div v-if="editing">
        <input
            type="button"
            class="btn btn-secondary ms-auto"
            data-bs-toggle="modal"
            data-bs-target="#editCommentModal"
            value="Edit"
            ref="editCommentModal" hidden />
        <CommentEditModal :editing="editing" @edit-comment="editComment" id="editCommentModal" />
    </div>
</template>

<script lang="ts">
import { Article, ArticleComment, NestedArticleComment } from "@/types.ts";
import { useArticleStore } from "@/store/articleStore.ts";
import { getHeaders, getUrl } from "@/utils.ts";
import CommentCreateModal from "@/components/CommentCreateModal.vue";
import CommentCard from "@/components/CommentCard.vue";
import CommentEditModal from "@/components/CommentEditModal.vue";
import { useUserStore } from "@/store/userStore.ts";

export default {
    components: {
        CommentEditModal,
        CommentCreateModal,
        CommentCard
    },
    data() {
        return {
            comments: [] as ArticleComment[],
            reply_to: null as ArticleComment | null,
            editing: null as ArticleComment | null,
            isLoading: true
        }
    },
    computed: {
        id(): number {
            return parseInt(this.$route.params.id as string)
        },
        article(): Article | undefined {
            return useArticleStore().articles.find((article) => article.id == this.id )
        },
        viewableComments(): NestedArticleComment[] {
            const viewable = this.comments.filter(c => c.reply_to === undefined) as NestedArticleComment[]
            viewable.forEach(comment => { comment.replies = this.buildCommentTree(comment) })
            return viewable
        },
        loggedIn(): boolean {
            return useUserStore().user !== null
        }
    },
    methods: {
        async createComment(comment: string) {
            const body: Record<string, string | number> = {'comment': comment}
            if (this.reply_to !== null) {
                body['reply_to'] = this.reply_to.id
            }

            const response = await fetch(getUrl() + `api/articles/${this.id}/comments/`, {
                'method': 'POST',
                'body': JSON.stringify(body),
                'headers': getHeaders()
            })
            if (response.ok) {
                const json = await response.json()
                this.comments.unshift(json as ArticleComment)
            }
        },
        async editComment(comment: string) {
            const response = await fetch(getUrl() + `api/articles/${this.id}/comments/${this.editing!.id}/`, {
                'method': 'PUT',
                body: JSON.stringify({'comment': comment}),
                headers: getHeaders()
            })
            if (response.ok) {
                const index = this.comments.findIndex(c => c.id === this.editing!.id)
                if (index != -1) {
                    this.comments[index].comment = comment
                }
            }
        },
        async deleteComment(id: number) {
            const response = await fetch(getUrl() + `api/articles/${this.id}/comments/${id}/`, {
                'method': 'DELETE',
                'headers': getHeaders()
            })
            if (response.ok) {
                const comment = this.comments.find(comment => comment.id == id) as NestedArticleComment
                const toDelete = this.flattenCommentTree(comment)
                toDelete.push(comment)

                this.comments = this.comments.filter(c => !toDelete.includes(c as NestedArticleComment))
            }
        },
        async onReply(comment: ArticleComment) {
            this.reply_to = comment
            const modal = this.$refs.createCommentModal as HTMLInputElement
            modal.click()
        },
        async onEdit(comment: ArticleComment) {
            this.editing = comment

            await this.$nextTick(() => {
                const modal = this.$refs.editCommentModal as HTMLInputElement
                modal.click()
            })
        },
        buildCommentTree(parent: NestedArticleComment): NestedArticleComment[] {
            const replies = this.comments.filter(c => c.reply_to?.id === parent.id) as NestedArticleComment[]
            replies.forEach(reply => { reply.replies = this.buildCommentTree(reply) })
            return replies
        },
        flattenCommentTree(parent: NestedArticleComment): NestedArticleComment[] {
            const flatMap: NestedArticleComment[] = []

            if (parent.replies) {
                parent.replies.forEach((reply: NestedArticleComment) => {
                    flatMap.push(reply)
                    flatMap.push(...this.flattenCommentTree(reply))
                })
            }

            return flatMap
        }
    },
    async mounted() {
        const response = await fetch(getUrl() + `api/articles/${this.id}/`)
        if (response.ok) {
            const json = await response.json()
            this.comments = json['comments']
            this.isLoading = false
        }
    }
}
</script>