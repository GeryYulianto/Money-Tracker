<script setup>
// defineProps({
//   msg: {
//     type: String,
//     required: true,
//   },
// })
</script>

<template>
    <h1 class="text-success text-center"> Login </h1>
    
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">

                        <form id="loginForm" action="">

                            <div class="form-group">
                                <label for="username"> Username </label>
                                <input type="username" class="form-control" id="username" placeholder="Username" required />
                            </div>

                            <div class="form-group">
                                <label for="password"> Password </label>
                                <input type="password" class="form-control" id="password" placeholder="Password" required />
                            </div>

                            <br>
                            <button class="btn btn-primary"> Login </button>
                        </form>

                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

