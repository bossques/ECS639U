<template>
    <div class="modal fade" :id="id" tabindex="-1" :aria-labelledby="id" aria-hidden="true" ref="commentModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" :id="id+'label'">Edit Comment</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"/>
                </div>
                <div class="modal-body form-group">
                    <label>Before</label>
                    <CommentCard :comment="editing" :modifiable=false :render-replies="false" :max-length="128" />

                    <label>After</label>
                    <textarea type="text" v-model="comment" class="form-control"/>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-success" data-bs-dismiss="modal" @click="emitSubmit">Edit</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { ArticleComment } from "@/types.ts";
import CommentCard from "@/components/CommentCard.vue";
import {PropType} from "vue";

export default {
    components: {
        CommentCard
    },
    props: {
        id: {
            type: String
        },
        editing: {
            type: Object as PropType<ArticleComment>,
            required: true
        }
    },
    data() {
        return {
            comment: ''
        }
    },
    methods: {
        async emitSubmit() {
            this.$emit('edit-comment', this.comment)
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