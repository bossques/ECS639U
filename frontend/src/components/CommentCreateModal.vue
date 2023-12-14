<template>
    <div class="modal fade" :id="id" tabindex="-1" :aria-labelledby="id" aria-hidden="true" ref="commentModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" :id="id+'label'">Create Comment</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"/>
                </div>
                <div class="modal-body form-group">
                    <div v-if="reply_to">
                        <label>Replying to</label>
                        <CommentCard :comment="reply_to" :modifiable=false :render-replies="false" :max-length="128" />
                    </div>

                    <label>Comment</label>
                    <textarea type="text" v-model="comment" class="form-control"/>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-success" data-bs-dismiss="modal" @click="emitSubmit">Comment</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { ArticleComment } from "@/types.ts";
import CommentCard from "@/components/CommentCard.vue";
import { PropType } from "vue";

export default {
    components: {
        CommentCard
    },
    props: {
        id: {
            type: String
        },
        reply_to: {
            type: null as unknown as PropType<ArticleComment | null>,
            required: false,
            default: null
        }
    },
    data() {
        return {
            comment: ''
        }
    },
    methods: {
        async emitSubmit() {
            this.$emit('create-comment', this.comment)
            this.resetForm()
        },
        resetForm() {
            this.comment = ''
            this.$emit('close')
        }
    },
    mounted() {
        const modal = this.$refs.commentModal as HTMLElement
        modal.addEventListener('hidden.bs.modal', this.resetForm)
    },
    beforeUnmount() {
        const modal = this.$refs.commentModal as HTMLElement
        modal.removeEventListener('hidden.bs.modal', this.resetForm)
    }
}
</script>