import pytest
from playwright.sync_api import expect, Page


def test_add_product_to_cart(page: Page) -> None:
    """Test adding a product to cart on the e-commerce platform"""
    try:
        # Navigate to the e-commerce platform
        page.goto("https://testathon.live/", timeout=30000)
        
        # Wait for page to load
        page.wait_for_selector(".shelf-container", timeout=10000)
        
        # Get the first product name
        first_product = page.locator(".shelf-item")
        product_name = first_product.inner_text()
        print(f"Product: {product_name}")
        
        # Add the product to cart
        page.locator(".shelf-item__buy-btn .add-to-cart").click()
        
        # Wait for cart to update
        page.wait_for_selector(".cart-count", timeout=5000)
        
        # Verify cart count updated
        cart_count = page.locator(".cart-count")
        expect(cart_count).to_have_text("1")
        print(f"Cart count: {cart_count.inner_text()}")
        
        # Open cart/mini-cart
        page.locator(".cart-icon").click()
        page.wait_for_selector(".mini-cart", timeout=5000)
        
        # Verify product is in cart
        cart_product_name = page.locator(".mini-cart .product-name").first.inner_text()
        assert cart_product_name == product_name, f"Expected {product_name}, got {cart_product_name}"
        print(f"Cart product: {cart_product_name}")
        
        mark_test_status("passed", f"Successfully added {product_name} to cart", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>").replace("'", "")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def test_product_search_functionality(page: Page) -> None:
    """Test search functionality on the e-commerce platform"""
    try:
        page.goto("https://testathon.live/", timeout=30000)
        
        # Search for a product
        search_input = page.locator(".search-input")
        search_input.fill("phone")
        search_input.press("Enter")
        
        # Wait for search results
        page.wait_for_selector(".search-results", timeout=10000)
        
        # Verify search results are displayed
        results_count = page.locator(".search-results .product-item")
        expect(results_count).to_have_count(at_least=1)
        
        result_count = results_count.count()
        print(f"Found {result_count} search results")
        
        mark_test_status("passed", f"Search returned {result_count} results", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>").replace("'", "")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def test_user_registration_flow(page: Page) -> None:
    """Test user registration process"""
    try:
        page.goto("https://testathon.live/", timeout=30000)
        
        # Navigate to registration
        page.locator(".register-btn").click()
        page.wait_for_selector(".registration-form", timeout=5000)
        
        # Fill registration form
        page.locator("[name='email']").fill(f"testuser{random.randint(1000,9999)}@example.com")
        page.locator("[name='password']").fill("TestPassword123!")
        page.locator("[name='confirmPassword']").fill("TestPassword123!")
        page.locator("[name='firstName']").fill("Test")
        page.locator("[name='lastName']").fill("User")
        
        # Submit registration
        page.locator(".register-submit").click()
        
        # Verify successful registration
        page.wait_for_selector(".welcome-message", timeout=10000)
        expect(page.locator(".welcome-message")).to_be_visible()
        
        mark_test_status("passed", "User registration successful", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>").replace("'", "")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def test_checkout_process(page: Page) -> None:
    """Test the checkout process"""
    try:
        page.goto("https://testathon.live/", timeout=30000)
        
        # Add product to cart
        page.locator(".product-item:first-child .add-to-cart").click()
        page.wait_for_selector(".cart-count", timeout=5000)
        
        # Proceed to checkout
        page.locator(".checkout-btn").click()
        page.wait_for_selector(".checkout-form", timeout=5000)
        
        # Fill checkout information
        page.locator("[name='shippingAddress']").fill("123 Test Street")
        page.locator("[name='city']").fill("Test City")
        page.locator("[name='zipCode']").fill("12345")
        page.select_option("[name='country']", "US")
        
        # Continue to payment
        page.locator(".continue-to-payment").click()
        page.wait_for_selector(".payment-form", timeout=5000)
        
        # Fill payment information
        page.locator("[name='cardNumber']").fill("4111111111111111")
        page.locator("[name='expiryDate']").fill("12/25")
        page.locator("[name='cvv']").fill("123")
        
        # Place order
        page.locator(".place-order").click()
        
        # Verify order confirmation
        page.wait_for_selector(".order-confirmation", timeout=10000)
        expect(page.locator(".order-confirmation")).to_be_visible()
        
        mark_test_status("passed", "Checkout process completed successfully", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>").replace("'", "")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def mark_test_status(status: str, reason: str, page: Page) -> None:
    """Mark test status in BrowserStack"""
    page.evaluate(
        "_ => {}", 
        f"browserstack_executor: {{\"action\": \"setSessionStatus\", \"arguments\": {{\"status\":\"{status}\", \"reason\": \"{reason}\"}}}}"
    )


# Run specific tests based on environment
if __name__ == "__main__":
    import random
    pytest.main([__file__, "-v"])