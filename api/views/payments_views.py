import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

class CreatePaymentIntentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            amount = int(request.data.get('amount'))  # amount should be in cents
            payment_method_id = request.data.get('paymentMethodId')

            stripe.api_key = settings.STRIPE_SECRET_KEY

            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method=payment_method_id,
                confirm=True,
            )

            return Response(status=status.HTTP_200_OK, data={'client_secret': intent.client_secret})

        except stripe.error.CardError as e:
            # Handle card errors
            body = e.json_body
            err = body.get('error', {})
            error_message = err.get('message')
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': error_message})

        except stripe.error.StripeError as e:
            # Handle other Stripe API errors
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': str(e)})

        except Exception as e:
            # Handle other generic errors
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': str(e)})