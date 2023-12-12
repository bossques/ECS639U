<template>
    <div class="container col-sm-6">
        <div v-if="saved" class="alert alert-success" role="alert">
            Your changes have been saved.
        </div>

        <form class="card" @submit.prevent="onSubmit" @dragover.prevent="(event: DragEvent) => { event.preventDefault() }" @drop.prevent="onDrop">
            <div class="card-body">
                <div class="form-group p-2">
                    <label>Profile Picture:</label>

                    <div class="text-center rounded p-2">
                        <img v-if="profileUrl" :src="profileUrl" alt="Profile Image" @click="onProfileClick" class="img-fluid col-sm-4">
                    </div>
                    <input type="file" @change="onFileChange" alt="Profile Image" class="form-control-file" accept="image/*" ref="fileInputRef">
                </div>
                <Error :error-messages="errors?.profile_image"/>

                <div class="form-group p-2">
                    <label>Email Address:</label>
                    <input type="email" v-model="form.email" class="form-control">
                </div>
                <Error :error-messages="errors?.email"/>

                <div class="form-group p-2">
                    <label>Date Of Birth:</label>
                    <input type="date" v-model="form.dateOfBirth" class="form-control">
                </div>
                <Error :error-messages="errors?.date_of_birth"/>
            </div>

            <div class="card-footer">
                <input type="submit" class="btn btn-success w-100" value="Save" />
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">
import { Ref, ref } from "vue";
import { BadRequestError, useUserStore } from "@/store/userStore";
import type { BadRequestResponse } from "@/types.ts";
import Error from "@/components/Error.vue";
const userStore = useUserStore();
const profileUrl = ref(userStore.user?.profile_url ?? null)
const fileInputRef = ref<HTMLInputElement | null>(null);
const errors = ref<BadRequestResponse>({});
const saved = ref<boolean>(false);

interface Form {
    profileImage: File | null;
    email: string;
    dateOfBirth: string;
}

const form: Ref<Form> = ref({
    profileImage: null,
    email: userStore.user?.email ?? '',
    dateOfBirth: userStore.user?.date_of_birth ?? ''
})

const onFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement
    if (target.files && target.files.length > 0) {
        form.value.profileImage = target.files[0];
        profileUrl.value = URL.createObjectURL(form.value.profileImage)
    }
}

const onProfileClick = () => {
    if (fileInputRef.value) {
        fileInputRef.value.click();
    }
}

const onDrop = (event: DragEvent) => {
    event.preventDefault()
    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
        form.value.profileImage = event.dataTransfer.files[0]
        profileUrl.value = URL.createObjectURL(form.value.profileImage)
    }
}

const onSubmit = async () => {
    errors.value = {}
    try {
        await userStore.modify(
            form.value.email,
            form.value.dateOfBirth,
            form.value.profileImage
        )
        saved.value = true;
    } catch (e) {
        saved.value = false;
        if (e instanceof BadRequestError) {
            errors.value = JSON.parse(e.message)
            return
        }
        throw e
    }
}

</script>