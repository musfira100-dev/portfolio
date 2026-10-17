from .models import FAQ


def faqs(request):
    """Footer ke FAQ section ke liye: sirf published FAQs, order ke mutabiq."""
    return {"faqs": list(FAQ.objects.filter(is_published=True))}