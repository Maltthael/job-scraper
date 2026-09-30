from playwright.async_api import async_playwright

async def buscar_remotar_playwright() -> list[dict]:
    url = "https://remotar.com.br/job?search=estagio"
    vagas = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, channel="msedge")
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            print("[Remotar Playwright] Acessando a página de vagas com o Edge...")
            await page.goto(url, wait_until="domcontentloaded", timeout=20000)

            selector_card = 'a[href*="/job/"]'
            await page.wait_for_selector(selector_card, timeout=10000)
            
            for _ in range(3):
                await page.evaluate("window.scrollBy(0, document.body.scrollHeight)") 
                await page.wait_for_timeout(1500)

            cards = await page.query_selector_all(selector_card)
            print(f"[Remotar Playwright] {len(cards)} cards encontrados!")

            links_vistos = set()

            for card in cards[:20]:
                href = await card.get_attribute("href")
                if not href or href in links_vistos:
                    continue

                links_vistos.add(href)
                link_completo = href if href.startswith("http") else f"https://remotar.com.br{href}"

                texto_card = await card.inner_text()
                linhas = [linha.strip() for linha in texto_card.split("\n") if linha.strip()]

                titulo = linhas[0] if linhas else "Vaga de Estágio Remoto"
                empresa = linhas[1] if len(linhas) > 1 else "Remotar"

                vagas.append({
                    "titulo": titulo,
                    "empresa": empresa,
                    "link": link_completo,
                    "fonte": "Remotar (Playwright)"
                })

        except Exception as e:
            print(f"[Remotar Playwright Exceção]: {e}")

        finally:
            await browser.close()

    return vagas