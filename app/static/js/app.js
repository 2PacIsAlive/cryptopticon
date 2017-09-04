var app = new Vue({
    el: '#app',
    data: function() {
        return {
            screen: "login",
            alertNewUserCreated: false,
            alertAlertCreated: false,
            user: {
                name: "",
                number: null,
                isAuthenticated: false
            },
            rules: {
                required: (value) => !!value || 'Required.'
            }
        }
    },
    methods: {
        signup: function() {
            app = this;
            // password stuff..
            $.ajax('/cryptopticon/users', {
                data: JSON.stringify({
                    username: this.user.name,
                    email: this.user.email
                }),
                contentType: 'application/json',
                method: "POST"
            }).done(function(response) {
                    app.alertNewUserCreated = false;
                    app.alertNewUserCreated = true;
                    app.user.isAuthenticated = true;
                    app.screen = "hub";
                }, "json")
                .fail(function() {
                    console.log("create new user failed!!")
                });
        },
        login: function() {
            app = this;
			// TODO...
            if (app.user.number === "+11234567890" || true) {
                $.ajax("/cryptopticon/users/" + "fixme" + "/alerts", {
                    method: "GET"
                }).done(function(response) {
                    app.alerts = response
                    console.log("alerts: " + app.networks)
                });
                app.user.isAuthenticated = true;
                app.screen = "hub";
            }
        },
        logout: function() {
            this.user.isAuthenticated = false;
            this.screen = "login";
        },
        changeScreen: function (screen) {
            app = this;
            if (app.user.isAuthenticated) {
                app.screen = screen;
            } else if (screen === "about" || screen === "signup") {
                app.screen = screen;
            } else {
                app.screen = "login";
            }
        }
    },
    mounted: function () {

    },
    computed: {

    }
});

