from playwright.sync_api import sync_playwright


def analyze_website(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            page = browser.new_page(
                viewport={
                    "width": 1440,
                    "height": 900
                }
            )

            response = page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            page.wait_for_timeout(2000)

            website_data = page.evaluate("""
                () => {
                    const headings = Array.from(
                        document.querySelectorAll(
                            "h1, h2, h3"
                        )
                    ).map(item => ({
                        tag: item.tagName,
                        text: item.innerText.trim()
                    }));

                    const images = Array.from(
                        document.querySelectorAll("img")
                    ).map(img => ({
                        src: img.src,
                        alt: img.alt
                    }));

                    const links = Array.from(
                        document.querySelectorAll("a")
                    ).map(link => ({
                        text: link.innerText.trim(),
                        href: link.href
                    }));

                    const sections = Array.from(
                        document.querySelectorAll(
                            "header, nav, main, section, footer"
                        )
                    ).map(section => ({
                        tag: section.tagName,
                        text: section.innerText
                            .trim()
                            .slice(0, 500)
                    }));

                    const styles = Array.from(
                        document.querySelectorAll("h1, h2, p, button")
                    ).slice(0, 50).map(element => {
                        const style = getComputedStyle(element);

                        return {
                            tag: element.tagName,
                            color: style.color,
                            background: style.backgroundColor,
                            fontSize: style.fontSize,
                            fontFamily: style.fontFamily
                        };
                    });

                    return {
                        title: document.title,
                        description:
                            document.querySelector(
                                'meta[name="description"]'
                            )?.content || "",
                        headings,
                        images,
                        links: links.slice(0, 50),
                        sections,
                        styles
                    };
                }
            """)

            website_data["status_code"] = (
                response.status if response else None
            )

            browser.close()

            return {
                "success": True,
                "data": website_data
            }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }