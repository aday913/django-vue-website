<template>
    <div class="tasks_container">
        <div class="add_task">
            <form v-on:submit.prevent="submitForm">
                <div class="form-group">
                    <label for="title">Title</label>
                    <input type="text" class="form-control" id="title" v-model="title">
                </div>
                <div class="form-group">
                    <label for="description">Description</label>
                    <textarea class="form-control" id="description" v-model="description"></textarea>
                </div>
                <div class="form-group">
                    <button type="submit">Add Task</button>
                </div>
            </form>
        </div>
        <div class="tasks_content">
            <h1>Tasks</h1>
            <ul class="tasks_list">
                <li v-for="task in tasks" :key="task.id">
                    <h2>{{ task.title }}</h2>
                    <p>{{ task.description }}</p>
                    <button @click="toggleTask(task)">
                        {{ task.completed ? 'Undo' : 'Complete' }}
                    </button>
                    <button @click="deleteTask(task)">Delete</button>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    export default {
        data() {
            return {
                // tasks
                name: "TasksComponent",
                tasks: [],
                title: '',
                description: '',
            }
        },
        mounted () {
            this.getData
        },
        methods: {
            ForcesUpdateComponent() {
                this.$forceUpdate();
            },
            async getData() {
                try {
                    axios({
                        method: 'get',
                        url: 'http://127.0.0.1:8000/api/tasks/'
                    }).then(response => this.tasks = response.data)
                } catch (error) {
                    // log the error
                    console.log(error);
                }
            },
            // async submitForm() {
            //     try {
            //         axios({
            //             method: 'post',
            //             url: 'http://127.0.0.1:8000/api/tasks/',
            //             data : {
            //                 title: this.title,
            //                 description: this.description,
            //                 completed: false
            //             }
            //         }).then(function (response) {console.log(response)})
            //     } catch (error) {
            //         console.log('there has been an error here')
            //         console.log(error.response.data)
            //     }
            // }
        },
    }
</script>