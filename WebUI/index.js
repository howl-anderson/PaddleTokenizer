// const api_host='http://127.0.0.1:5000'

var vm = new Vue({
    el: '#app',
    data: {
        server: "http://127.0.0.1:5000",
        message: "王小明在北京的清华大学读书。",

        token_list: {},
    },
    created: function () {},
    methods: {
        send_tokenize_request: function () {
            vm.axios.get(vm.server + '/single_tokenizer', {
                params: {
                    'message': vm.message
                }
            })
                .then(function (response) {
                    console.log(response.data);
                    vm.token_list = response.data;
                })
                .catch(function (error) {
                    console.log(error);
                })
                .then(function () {
                    // always executed
                });
        }
    }
})
