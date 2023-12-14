<template>
    <div
        class="d-flex align-items-center p-1 border"
        v-if="comment"
        @mouseover="isHovered = true"
        @mouseleave="isHovered = false" >
        <div class="profile-picture rounded border">
            <img
                :src="comment.belongs_to.profile_url"
                v-if="comment.belongs_to.profile_url"
                alt="Profile Image"
                class="profile-picture rounded" />
        </div>

        <div class="d-flex flex-column px-3">
            <div class="d-flex flex-row align-baseline">
                <h6>{{ comment.belongs_to.username }}</h6>
                <small class="px-1">{{ formatDate(comment.created_at) }}</small>


                <small v-if="renderReplies && replies.length > 0">
                    <a href='#' @click.prevent="displayReplies = !displayReplies">
                        {{ displayReplies ? 'hide replies' : 'show replies'}}
                    </a>
                </small>
            </div>

            <p v-if="maxLength !== undefined && comment.comment.length > maxLength">
                {{ comment.comment.slice(0, maxLength-3) }}...
            </p>
            <p v-else>
                {{ comment.comment }}
            </p>
        </div>

        <div class="ms-auto p-1" v-show="(isHovered && (canModify || canReply)) && modifiable">
            <div class="dropend">
                <button type="button" class="btn btn-secondary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">

                </button>
                <ul class="dropdown-menu">
                    <li v-if="canReply">
                        <a class="dropdown-item" @click.prevent="$emit('reply', comment)">Reply</a>
                    </li>
                    <li v-if="canModify">
                        <a class="dropdown-item" @click.prevent="$emit('edit', comment)">Edit</a>
                    </li>
                    <li v-if="canModify">
                        <a class="dropdown-item" @click.prevent="$emit('delete', comment.id)">Delete</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <div v-if="renderReplies && displayReplies" v-for="reply in replies" class="ps-4">
        <!-- forward events -->
        <CommentCard
            :comment="reply"
            @delete="(id: number) => $emit('delete', id)"
            @edit="(c: any) => $emit('edit', c)"
            @reply="(c: any) => $emit('reply', c)"
        />
    </div>
</template>

<script lang="ts">
import { ArticleComment, NestedArticleComment } from "@/types.ts";
import { useUserStore } from "@/store/userStore.ts";
import { PropType } from "vue";
export default {
    data() {
        return {
            isHovered: false,
            displayReplies: false
        }
    },
    props: {
        comment: Object as PropType<ArticleComment | NestedArticleComment>,
        modifiable: {
            type: Boolean,
            default: true
        },
        renderReplies: {
            type: Boolean,
            default: true
        },
        maxLength: {
            type: Object as PropType<number | undefined>,
            default: undefined
        }
    },
    computed: {
        canModify() {
            return useUserStore().user?.id === this.comment?.belongs_to?.id
        },
        canReply() {
            return useUserStore().user !== null
        },
        replies() {
            if (this.comment !== undefined && 'replies' in this.comment) {
                return this.comment.replies
            }
            return []
        }
    },
    methods: {
        formatDate(datetimeString: string) {
            const datetime = new Date(datetimeString)
            const options: Intl.DateTimeFormatOptions = {year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'}

            return datetime.toLocaleString('en-US', options)
        },
    }
}
</script>

<style scoped>
.profile-picture {
    width: 60px;
    height: 60px;
    object-fit: cover;
    align-self: flex-start;
}

</style>