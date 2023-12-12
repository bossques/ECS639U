<template>
    <div v-if="errorMessages && errorMessages.length > 0">
        <div v-for="error in errorMessages">
            <p>{{ error.message }}</p>
        </div>
    </div>
</template>

<script lang="ts">
import type { ErrorMessage } from "@/types.ts";

export default {
    props: {
        errorMessages: {
            type: Array as () => ErrorMessage[],
            default: () => [],
        },
    }
}
</script>