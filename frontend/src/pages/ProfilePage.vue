<template>
    <div class="row col-sm-12">
        <div class="col-sm-6 offset-sm-1" @drop.prevent="onDrop">
            <div v-if="saved" class="alert alert-success" role="alert">
                Your changes have been saved.
            </div>

            <div class="card">
                <div class="card-title">
                    <h5 class="px-3">Your Profile</h5>
                </div>

                <div class="card-body">
                    <div class="form-group">
                        <label>Profile Picture:</label>
                        <div class="text-center p-2 border">
                            <img v-if="profileUrl" :src="profileUrl" alt="Profile Image" class="img-fluid col-sm-4"/>
                        </div>
                        <input type="file" alt="Profile Image" class="form-control-file" accept="image/*" @change="onFileChange"/>
                    </div>
                    <Error :error-messages="formErrors?.profile_image"/>

                    <div class="form-group">
                        <label>Email Address:</label>
                        <input type="email" v-model="form.email" class="form-control">
                    </div>
                    <Error :error-messages="formErrors?.email"/>

                    <div class="form-group">
                        <label>Date Of Birth:</label>
                        <input type="date" v-model="form.dateOfBirth" class="form-control">
                    </div>
                    <Error :error-messages="formErrors?.date_of_birth"/>
                </div>

                <div class="card-footer">
                    <input type="submit" class="btn btn-success w-100" value="Save" @click="onSubmit" />
                </div>
            </div>
        </div>

        <div class="offset-sm-1 col-sm-3 card">
            <div class="card-title">
                <h5 class="px-3">Your Favourite Categories</h5>
            </div>

            <div class="card-body">
                <div v-for="category in categories" :key="category.id" class="form-check form-switch">
                    <input
                        type="checkbox"
                        class="form-check-input"
                        :value="category.id"
                        :checked="category.enabled"
                        @click.prevent="onCategoryToggle(category)" />
                    <label>{{ category.name }}</label>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useArticleStore } from "@/store/articles.ts";
import { BadRequestError, useUserStore } from "@/store/userStore.ts";
import { ArticleCategory, BadRequestResponse } from "@/types.ts";
import Error from "@/components/Error.vue";

type ExtendedArticleCategory = ArticleCategory & { enabled: boolean; }
type Form = { profileImage: File | null, email: string, dateOfBirth: string }

export default defineComponent({
    components: {
        Error
    },
    setup() {
        const userStore = useUserStore()

        const form = ref<Form>({
            profileImage: null,
            email: userStore.user?.email ?? '',
            dateOfBirth: userStore.user?.date_of_birth ?? ''
        })
        const formErrors = ref<BadRequestResponse>({})
        const profileUrl = ref(userStore.user?.profile_url ?? null)
        const saved = ref(false);

        return {
            form,
            formErrors,
            profileUrl,
            saved
        }
    },
    computed: {
        categories(): ExtendedArticleCategory[] {
            const userStore = useUserStore()
            const favouriteCategories = userStore?.user?.favourite_categories

            return useArticleStore().categories.map(category => ({
                ...category,
                enabled: favouriteCategories?.some(c => c.id === category.id) ?? false
            }))
        }
    },
    methods: {
        onCategoryToggle(category: ArticleCategory) {
            useUserStore().toggleCategory(category)
        },
        onDrop(event: DragEvent) {
            if (event.dataTransfer && event.dataTransfer.files.length > 0) {
                this.form.profileImage = event.dataTransfer.files[0]
                this.profileUrl = URL.createObjectURL(this.form.profileImage)
            }
        },
        onFileChange(event: Event) {
            const target = event.target as HTMLInputElement
            if (target.files && target.files.length > 0) {
                this.form.profileImage = target.files[0]
                this.profileUrl = URL.createObjectURL(this.form.profileImage)
            }
        },
        async onSubmit() {
            this.formErrors = {}

            try {
                await useUserStore().modify(this.form.email, this.form.dateOfBirth, this.form.profileImage)
                this.saved = true
            } catch (e) {
                this.saved = false
                if (e instanceof BadRequestError) {
                    this.formErrors = JSON.parse(e.message)
                    return
                }
                throw e
            }
        }
    }
})

</script>