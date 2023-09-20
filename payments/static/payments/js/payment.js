document.addEventListener("DOMContentLoaded", async () => {
    // Stripe Integration

    const addMessage = (message) => {
        const messagesDiv = document.querySelector("#messages");
        messagesDiv.style.display = "block";
        const messageWithLinks = addDashboardLinks(message);
        messagesDiv.innerHTML += `> ${messageWithLinks}<br>`;
        console.log(`Debug: ${message}`);
    }


    const addDashboardLinks = (message) => {
        const piDashboardBase =
            "https://dashboard.stripe.com/payments";
        return message.replace(
            /(pi_(\S*)\b)/g,
            `<a href="${piDashboardBase}/$1" target="_blank">$1</a>`
        );
    }

    let { data } = await fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            query: `
                query StripePublishableKey {
                    stripePublishableKey {
                        publishableKey
                    }
                }
            `,
            variables: {
                now: new Date().toISOString(),
            },
        }),
    }).then((res) => res.json());
    if (!data.stripePublishableKey.publishableKey) {
        addMessage(
            "No publishable key returned from the server. Please check `.env` and try again"
        );
        alert(
            "Please set your Stripe publishable API key"
        );
    }

    const stripe = Stripe(
        data.stripePublishableKey.publishableKey,
        {
            apiVersion: "2022-11-15",
        }
    );

    const elements = stripe.elements();

    const card = elements.create("card");

    card.mount("#card-element");

    const form = document.getElementById("payment-form");
    let submitted = false;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        if (submitted) {
            return;
        }

        submitted = true;

        form.querySelector("button").disabled = true;
        let package = document.querySelector("#package").value;
        const clientSecret = await fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                query: `
                        mutation StripeCreateIntent {
                            stripeCreateIntent(amount: ${package}, currency: "usd", paymentMethodType: "card"){
                                    clientSecret
                            }
                        }
                    `,
                variables: {
                    now: new Date().toISOString(),
                },
            }),
        }).then((res) => res.json());

        addMessage(`Client secret returned.`);
        const nameInput = document.querySelector("#name");
        const { error: stripeError, paymentIntent } =
            await stripe.confirmCardPayment(
                clientSecret.data.stripeCreateIntent.clientSecret,
                {
                    payment_method: {
                        card: card,
                        billing_details: {
                            name: nameInput.value,
                        },
                    },
                }
            );

        if (stripeError) {
            addMessage(stripeError.message);
            submitted = false;
            form.querySelector("button").disabled = false;
            return;
        }

        const paymentSuccess = await fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                query: `
                    mutation StripePaymentSuccess($intentId: String!,$status:String!) {
                        stripePaymentSuccess(
                            intentId: $intentId,
                            status: $status
                        ) {
                            success
                            message
                        }
                    }
                `,
                variables: {
                    intentId: paymentIntent.id,
                    status: paymentIntent.status
                },
            }),
        }).then((res) => res.json());
        addMessage(
            `Payment ${paymentIntent.status}: ${paymentIntent.id}`
        );
        alert(paymentSuccess.data.stripePaymentSuccess.message)
    });


    // PayPal Buttom
    paypal.Buttons({
        onClick: async (data, actions) => {
            let package = parseFloat(document.querySelector("#package").value).toFixed(2)
            if (package == "") {
                return actions.reject();
            } else {
                return actions.resolve();
            }
        },
        fundingSource: paypal.FUNDING.PAYPAL,

        createOrder: async (data, actions) => {
            let package = parseFloat(document.querySelector("#package").value).toFixed(2)
            let resp = await fetch("/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    query: `
                            mutation PayPalCreateOrder($amount: Float!) {
                                paypalCreateOrder(amount: $amount) {
                                    id
                                    status
                                }
                            }
                        `,
                    variables: {
                        amount: package,
                    },
                }),
            }).then((res) => res.json());
            return resp.data.paypalCreateOrder.id;
        },
        onApprove: async (data, actions) => {
            let capture = await fetch("/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    query: `
                            mutation PayPalCapturePayment($orderId: String!) {
                                paypalCapturePayment(orderId: $orderId){
                                    id
                                    status
                                }
                            }
                        `,
                    variables: {
                        orderId: data.orderID,
                    },
                }),
            }).then((res) => res.json());
            if (capture.data.paypalCapturePayment.status == "COMPLETED") {
                alert(`Payment for order ${capture.data.paypalCapturePayment.id} is completed successfully!`)
            } else {
                alert(`Payment for order ${capture.data.paypalCapturePayment.id} failed!`)
            }
        },
        onError: (err) => {
            console.log(err.message);
        },
        onCancel: async (data, actions) => {
            let cancel = await fetch("/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    query: `
                            mutation PayPalCancelOrder($orderId: String!) {
                                paypalCancelOrder(orderId: $orderId){
                                    id
                                    status
                                }
                            }
                        `,
                    variables: {
                        orderId: data.orderID,
                    },
                }),
            }).then((res) => res.json());
            console.log("Data", cancel);
            alert(`Order canceled: ${data.orderID}`)
        }
    }).render('#paypal-button-container');
});