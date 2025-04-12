<script setup>
import { ref } from 'vue';
import axios from 'axios';

const emit = defineEmits(['solved']);

const props = defineProps({
    challenge: {
        type: Object,
        required: true,
        default: () => ({
            id: 0,
            name: "",
            story: "",
            description: "",
            difficulty: "",
            solved: false,
            solved_timestamp: null,
        })
    }
});

const flag = ref('');
const showModal = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const submitFlag = async (submittedFlag) => {
    try {
        const response = await axios.post(`/api/v1/challenges/${props.challenge.id}/solve`, {
            flag: submittedFlag,
        });

        successMessage.value = "Correct flag!";
        errorMessage.value = '';

        // Wait 2 seconds so user sees the message before closing modal & refreshing
        setTimeout(() => {
            successMessage.value = '';
            showModal.value = false;
            emit('solved');
        }, 2000);

    } catch (error) {
        if (error.response && error.response.status === 400) {
            errorMessage.value = "Incorrect flag. Try again.";
        } else {
            errorMessage.value = "An error occurred while submitting the flag.";
            console.error("Error submitting flag:", error);
        }

        successMessage.value = '';

        setTimeout(() => {
            errorMessage.value = '';
        }, 5000);
    }

};
</script>

<template>
    <div class="col-xl-4 col-lg-4 col-md-6 text-center">
        <div class="card my-3 shadow-lg align-items-center challenge-card">
            <div class="card-body w-75">
                <h5 class="card-title pb-3">{{ challenge.name }}</h5>
                <p class="card-text text-start">
                    <strong>Status: </strong>
                    <span :class="challenge.solved ? 'text-success' : 'text-danger'">
                        <i :class="challenge.solved ? 'bi-check-circle-fill' : 'bi-x-circle-fill'"></i>
                        {{ challenge.solved ? 'Solved' : 'Unsolved' }}
                    </span>
                </p>
                <p class="card-text text-start">
                    <strong>Difficulty: </strong> {{ challenge.difficulty }}
                </p>
                <button class="btn btn-primary" @click="showModal = true">View Details</button>
            </div>
        </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" tabindex="-1" :class="{ show: showModal }" style="display: block;" v-if="showModal">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title text-center">{{ challenge.name }}</h5>
                    <button type="button" class="btn-close" @click="showModal = false"></button>
                </div>
                <div class="modal-body">
                    <p><strong>Story:</strong> {{ challenge.story }}</p>
                    <p><strong>Description:</strong> {{ challenge.description }}</p>

                    <div v-if="!challenge.solved">
                        <!-- Success Message -->
                        <div v-if="successMessage" class="alert alert-success" role="alert">
                            {{ successMessage }}
                        </div>

                        <!-- Error Message -->
                        <div v-if="errorMessage" class="alert alert-danger" role="alert">
                            {{ errorMessage }}
                        </div>

                        <div class="mb-3">
                            <label for="flagInput" class="form-label">Submit Flag</label>
                            <input type="text" id="flagInput" class="form-control shadow-sm" v-model="flag"
                                placeholder="Enter your flag here" :disabled="!!successMessage" />
                        </div>
                        <button class="btn btn-success" @click="submitFlag(flag)">Submit</button>
                    </div>

                    <!-- Already solved message -->
                    <div v-else class="alert alert-info">
                        🎉 You’ve already solved this challenge. Great job!
                    </div>
                </div>

                <div class="modal-footer">
                    <button class="btn btn-secondary" @click="showModal = false">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal backdrop -->
    <div class="modal-backdrop fade show" v-if="showModal"></div>
</template>

<style scoped>
.challenge-card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    border-radius: 12px;
    border: none;
}

.challenge-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0.75rem 1.5rem rgba(0, 0, 0, 0.15);
}

.card-title {
    font-weight: bold;
    font-size: 1.25rem;
}

.modal {
    display: none;
    background-color: rgba(0, 0, 0, 0.5);
}

.modal.show {
    display: block;
}

.modal-dialog {
    margin-top: 10vh;
    /* Push modal down a bit */
}

.modal-content {
    border-radius: 10px;
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.2);
}

.modal.fade .modal-content {
    animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: scale(0.98);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}

button.btn {
    transition: background-color 0.2s ease, transform 0.1s ease;
}
</style>