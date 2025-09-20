import pytest   
from playwright.sync_api import expect, Page 
import random
import time

def test_add_product_to_cart(page: Page) -> None:
    """Test adding a product to cart on the e-commerce platform"""
    try:
        # Navigate to the e-commerce platform
        page.goto("https://testathon.live/", timeout=30000)
        
        # Wait for page to load and products to be visible
        page.wait_for_selector("[data-test='product']", timeout=10000)
        
        # Get the first product name and price
        first_product = page.locator("[data-test='product']").first
        product_name = first_product.locator("[data-test='product-name']").inner_text()
        product_price = first_product.locator("[data-test='product-price']").inner_text()
        
        print(f"Product: {product_name}, Price: {product_price}")
        
        # Add the product to cart
        first_product.locator("[data-test='add-to-cart']").click()
        
        # Wait for cart to update - look for cart badge or counter
        page.wait_for_selector("[data-test='cart-count']", timeout=5000)
        
        # Verify cart count updated
        cart_count = page.locator("[data-test='cart-count']")
        expect(cart_count).to_have_text("1")
        print(f"Cart count: {cart_count.inner_text()}")
        
        # Navigate to cart page
        page.locator("[data-test='cart-link']").click()
        page.wait_for_selector("[data-test='cart-page']", timeout=5000)
        
        # Verify product is in cart
        cart_product_name = page.locator("[data-test='cart-item-name']").first.inner_text()
        cart_product_price = page.locator("[data-test='cart-item-price']").first.inner_text()
        
        assert cart_product_name == product_name, f"Expected {product_name}, got {cart_product_name}"
        assert cart_product_price == product_price, f"Expected {product_price}, got {cart_product_price}"
        
        print(f"Cart product: {cart_product_name}, Price: {cart_product_price}")
        
        mark_test_status("passed", f"Successfully added {product_name} to cart", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>").replace("'", "")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def test_product_search_functionality(page: Page) -> None:
    """Test search functionality on the e-commerce platform"""
    try:
        page.goto("https://testathon.live/", timeout=30000)
        
        # Wait for search input to be visible
        page.wait_for_selector("[data-test='search-input']", timeout=5000)
        
        # Search for a product
        search_input = page.locator("[data-test='search-input']")
        search_input.fill("phone")
        search_input.press("Enter")
        
        # Wait for search results
        page.wait_for_selector("[data-test='search-results']", timeout=10000)
        
        # Verify search results are displayed
        results = page.locator("[data-test='product']")
        expect(results).to_have_count(at_least=1)
        
        result_count = results.count()
        print(f"Found {result_count} search results")
        
        # Verify results contain search term
        first_result_name = results.first.locator("[data-test='product-name']").inner_text()
        assert "phone" in first_result_name.lower(), f"Search term not found in result: {first_result_name}"
        
        mark_test_status("passed", f"Search returned {result_count} results containing 'phone'", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>").replace("'", "")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def test_user_registration_flow(page: Page) -> None:
    """Test user registration process"""
    try:
        page.goto("https://testathon.live/", timeout=30000)
        
        # Navigate to registration
        page.locator("[data-test='register-link']").click()
        page.wait_for_selector("[data-test='registration-form']", timeout=5000)
        
        # Generate random user data
        random_email = f"testuser{random.randint(1000,9999)}@example.com"
        
        # Fill registration form
        page.locator("[data-test='email-input']").fill(random_email)
        page.locator("[data-test='password-input']").fill("TestPassword123!")
        page.locator("[data-test='confirm-password-input']").fill("TestPassword123!")
        page.locator("[data-test='first-name-input']").fill("Test")
        page.locator("[data-test='last-name-input']").fill("User")
        
        # Submit registration
        page.locator("[data-test='register-submit']").click()
        
        # Verify successful registration
        page.wait_for_selector("[data-test='welcome-message']", timeout=10000)
        expect(page.locator("[data-test='welcome-message']")).to_be_visible()
        
        # Verify user is logged in
        expect(page.locator("[data-test='user-profile']")).to_be_visible()
        
        mark_test_status("passed", f"User registration successful for {random_email}", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>").replace("'", "")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def test_checkout_process(page: Page) -> None:
    """Test the checkout process"""
    try:
        page.goto("https://testathon.live/", timeout=30000)
        
        # Add product to cart
        page.wait_for_selector("[data-test='product']", timeout=10000)
        page.locator("[data-test='product']").first.locator("[data-test='add-to-cart']").click()
        
        # Wait for cart to update
        page.wait_for_selector("[data-test='cart-count']", timeout=5000)
        
        # Proceed to checkout
        page.locator("[data-test='checkout-button']").click()
        page.wait_for_selector("[data-test='checkout-form']", timeout=5000)
        
        # Fill checkout information
        page.locator("[data-test='shipping-address-input']").fill("123 Test Street")
        page.locator("[data-test='city-input']").fill("Test City")
        page.locator("[data-test='zipcode-input']").fill("12345")
        page.locator("[data-test='country-select']").select_option("US")
        
        # Continue to payment
        page.locator("[data-test='continue-to-payment']").click()
        page.wait_for_selector("[data-test='payment-form']", timeout=5000)
        
        # Fill payment information
        page.locator("[data-test='card-number-input']").fill("4111111111111111")
        page.locator("[data-test='expiry-date-input']").fill("12/25")
        page.locator("[data-test='cvv-input']").fill("123")
        page.locator("[data-test='card-name-input']").fill("Test User")
        
        # Place order
        page.locator("[data-test='place-order']").click()
        
        # Verify order confirmation
        page.wait_for_selector("[data-test='order-confirmation']", timeout=15000)
        expect(page.locator("[data-test='order-confirmation']")).to_be_visible()
        
        # Verify order details
        order_number = page.locator("[data-test='order-number']").inner_text()
        print(f"Order placed successfully. Order number: {order_number}")
        
        mark_test_status("passed", f"Checkout process completed. Order #{order_number}", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>").replace("'", "")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def test_product_filtering(page: Page) -> None:
    """Test product filtering functionality"""
    try:
        page.goto("https://testathon.live/", timeout=30000)
        
        # Wait for filters to load
        page.wait_for_selector("[data-test='filter-category']", timeout=5000)
        
        # Apply a filter
        page.locator("[data-test='filter-category']").select_option("electronics")
        page.locator("[data-test='apply-filters']").click()
        
        # Wait for filtered results
        page.wait_for_selector("[data-test='filtered-products']", timeout=10000)
        
        # Verify products are filtered
        products = page.locator("[data-test='product']")
        expect(products).to_have_count(at_least=1)
        
        # Check if products belong to the filtered category
        first_product_category = page.locator("[data-test='product-category']").first.inner_text()
        assert "electronics" in first_product_category.lower(), f"Expected electronics, got {first_product_category}"
        
        print(f"Filter applied successfully. First product category: {first_product_category}")
        
        mark_test_status("passed", "Product filtering works correctly", page)
        
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




def test_basic_page_loading(page: Page) -> None:
    """Test that the page loads basic content"""
    try:
        # Navigate to the e-commerce platform
        page.goto("https://testathon.live/", timeout=30000)
        
        # Wait for page to load completely (wait for network idle)
        page.wait_for_load_state('networkidle')
        
        # Check page title
        expect(page).to_have_title("StackDemo")
        print("✓ Page title is correct")
        
        # Check if page has any content
        body_content = page.locator("body").inner_text()
        assert len(body_content.strip()) > 0, "Page content is empty"
        print("✓ Page has content")
        
        # Take screenshot for debugging
        page.screenshot(path="screenshots/page_loaded.png")
        
        mark_test_status("passed", "Page loaded successfully", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def test_find_interactive_elements(page: Page) -> None:
    """Test finding interactive elements on the page"""
    try:
        page.goto("https://testathon.live/", timeout=30000)
        page.wait_for_load_state('networkidle')
        
        print("🔍 Looking for interactive elements...")
        
        # Look for common interactive elements
        buttons = page.locator("button")
        links = page.locator("a")
        inputs = page.locator("input, select, textarea")
        
        print(f"Found {buttons.count()} buttons, {links.count()} links, {inputs.count()} inputs")
        
        # Try to find elements by common patterns
        common_selectors = [
            "[class*='product']", "[class*='card']", "[class*='item']",
            "[class*='btn']", "[class*='button']", "[class*='add']",
            "[class*='cart']", "[class*='search']", "[class*='menu']",
            "[class*='nav']", "[class*='header']", "[class*='footer']"
        ]
        
        for selector in common_selectors:
            elements = page.locator(selector)
            if elements.count() > 0:
                print(f"Found {elements.count()} elements with selector: {selector}")
                for i in range(min(elements.count(), 2)):
                    element = elements.nth(i)
                    text = element.inner_text().strip()[:50]
                    if text:
                        print(f"  - '{text}...'")
        
        # Try to click first button if available
        if buttons.count() > 0:
            first_button = buttons.first
            button_text = first_button.inner_text().strip()
            print(f"Clicking button: '{button_text}'")
            first_button.click()
            time.sleep(2)  # Wait to see what happens
            print("Button clicked successfully")
        
        mark_test_status("passed", "Interactive elements test completed", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def test_page_structure_analysis(page: Page) -> None:
    """Analyze the page structure to understand what's available"""
    try:
        page.goto("https://testathon.live/", timeout=30000)
        page.wait_for_load_state('networkidle')
        
        print("📊 Analyzing page structure...")
        
        # Get all elements with classes
        all_elements = page.locator("*")
        class_elements = []
        
        # Sample some elements to understand structure
        for i in range(min(all_elements.count(), 100)):
            element = all_elements.nth(i)
            class_name = element.get_attribute("class") or ""
            tag_name = element.evaluate("el => el.tagName.toLowerCase()")
            
            if class_name:
                class_elements.append((tag_name, class_name))
        
        # Print unique classes
        unique_classes = set(class_elements)
        print("Unique element classes found:")
        for tag, cls in sorted(unique_classes)[:20]:  # Show first 20
            print(f"  {tag}.{cls}")
        
        # Look for data attributes
        data_attrs = page.locator("[data-]")
        print(f"Found {data_attrs.count()} elements with data attributes")
        
        for i in range(min(data_attrs.count(), 10)):
            element = data_attrs.nth(i)
            attributes = element.evaluate("""
                el => {
                    const attrs = {};
                    for (let attr of el.attributes) {
                        if (attr.name.startsWith('data-')) {
                            attrs[attr.name] = attr.value;
                        }
                    }
                    return attrs;
                }
            """)
            if attributes:
                print(f"  Data attributes: {attributes}")
        
        mark_test_status("passed", "Page structure analysis completed", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def test_javascript_content_loading(page: Page) -> None:
    """Test if content is loaded via JavaScript after page load"""
    try:
        page.goto("https://testathon.live/", timeout=30000)
        
        # Wait for different states to see when content appears
        page.wait_for_load_state('domcontentloaded')
        print("DOM content loaded")
        
        # Wait a bit for JavaScript to execute
        time.sleep(3)
        
        # Check if content appears after some time
        body_text = page.locator("body").inner_text()
        print(f"Body content after 3 seconds: {body_text[:200]}...")
        
        # Wait for network idle
        page.wait_for_load_state('networkidle')
        print("Network idle state reached")
        
        # Check content again
        body_text_after = page.locator("body").inner_text()
        print(f"Body content after network idle: {body_text_after[:200]}...")
        
        # Take screenshots at different stages
        page.screenshot(path="screenshots/dom_loaded.png")
        time.sleep(2)
        page.screenshot(path="screenshots/after_wait.png")
        
        mark_test_status("passed", "JavaScript content loading test completed", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def test_element_visibility_check(page: Page) -> None:
    """Check what elements become visible over time"""
    try:
        page.goto("https://testathon.live/", timeout=30000)
        
        # Check visibility at different intervals
        for seconds in [1, 2, 3, 5, 10]:
            time.sleep(1)
            print(f"\nAfter {seconds} seconds:")
            
            # Count visible elements
            visible_elements = page.locator(":visible")
            print(f"  Visible elements: {visible_elements.count()}")
            
            # Check for specific element types
            for element_type in ["button", "a", "input", "div"]:
                elements = page.locator(element_type)
                visible_count = elements.count()
                if visible_count > 0:
                    print(f"  {element_type}: {visible_count}")
        
        # Final check after waiting
        page.wait_for_timeout(5000)  # Wait 5 more seconds
        final_visible = page.locator(":visible").count()
        print(f"\nFinal visible elements: {final_visible}")
        
        if final_visible > 10:  # If we have reasonable content
            print("✓ Content loaded successfully")
        else:
            print("⚠ Limited content visible - may be a loading issue")
        
        mark_test_status("passed", "Element visibility check completed", page)
        
    except Exception as err:
        error = str(err).split("Call log:")[0].replace("\n", " ").replace(":", "=>")
        mark_test_status("failed", error, page)
        raise pytest.fail(error)


def mark_test_status(status: str, reason: str, page: Page) -> None:
    """Mark test status in BrowserStack"""
    try:
        page.evaluate(
            "_ => {}", 
            f"browserstack_executor: {{\"action\": \"setSessionStatus\", \"arguments\": {{\"status\":\"{status}\", \"reason\": \"{reason}\"}}}}"
        )
    except:
        # If BrowserStack integration fails, just print for local testing
        print(f"Test status: {status} - {reason}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
if __name__ == "__main__":
    pytest.main([__file__, "-v"])