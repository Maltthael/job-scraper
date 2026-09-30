from playwright.async_api import async_playwright

async def buscar_gupy_playwright(termo: str = "estagio") -> list[dict]:
    url = f"https://portal.gupy.io/job-search?jobName={termo}"
    vagas = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, channel="msedge")
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        page = await context.new_page()
        
        try:
            print("[Gupy Playwright] Acessando o portal de vagas...")
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            await page.wait_for_timeout(3000)
            
            
            for i in range(1, 5):
                await page.evaluate(f"window.scrollTo(0, {i * 400})")
                await page.wait_for_timeout(800)
            
            selector_card = 'a[href*="/job"], a[data-testid="job-card-link"]'
            await page.wait_for_selector(selector_card, state="attached", timeout=15000)
            
            
            cards = await page.query_selector_all(selector_card)
            print(f"[Gupy Playwright] {len(cards)} elementos encontrados no DOM!")
            
            link_vistos = set()
            
            for card in cards:
                href = await card.get_attribute("href")
                if not href or href in link_vistos:
                    continue
                
                link_vistos.add(href)
                link_completo = href if href.startswith("http") else f"https://portal.gupy.io{href}"
                
                texto = await card.inner_text()
                linhas = [l.strip() for l in texto.split("\n") if l.strip()]

                titulo = linhas[0] if linhas else "Vaga Gupy"
                empresa = linhas[1] if len(linhas) > 1 else "Gupy Partner"

                vagas.append({
                    "titulo": titulo,
                    "empresa": empresa,
                    "link": link_completo,
                    "fonte": "Gupy (Playwright)"
                })

        except Exception as e:
            print(f"[Gupy Playwright Exceção]: {e}")
        finally:
            await browser.close()

    print(f"[Gupy Playwright] Total de vagas únicas: {len(vagas)}")
    return vagas