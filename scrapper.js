// scrapper.js
const { chromium } = require("playwright");

(async () => {
  const query = process.argv[2]; // tak query from CLI args
  if (!query) {
    console.error(JSON.stringify({ error: "No query provided" }));
    process.exit(1);
  }

  const url = `https://shop.preussenapotheke.de/suche/?search-term=${encodeURIComponent(query)}`;
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    await page.goto(url, { timeout: 60000 });

    // wait for products to load
    await page.waitForSelector(".col-lg-3.col-md-4.col-sm-2.mb-1", { timeout: 30000 });

    const products = await page.$$eval(".col-lg-3.col-md-4.col-sm-2.mb-1", (cards) =>
      cards.map(card => {
        const nameEl = card.querySelector(".product__name a");
        const manufacturerEl = card.querySelector(".product__manufacturer");
        const priceEl = card.querySelector(".product__price");
        const linkEl = card.querySelector(".product__name a");

        let link = linkEl ? linkEl.getAttribute("href") : null;
        let pzn = null;
        if (link && link.includes("/produkt/")) {
          const match = link.match(/\/produkt\/(\d+)\//);
          if (match) {
            pzn = match[1]; // extract PZN
          }
        }

        return {
          name: nameEl ? nameEl.innerText.trim() : null,
          manufacturer: manufacturerEl ? manufacturerEl.innerText.trim() : null,
          price: priceEl ? priceEl.innerText.trim() : null,
          link,
          pzn
        };
      })
    );

    console.log(JSON.stringify({ query, results: products }));
  } catch (err) {
    console.error(JSON.stringify({ error: err.message }));
  } finally {
    await browser.close();
  }
})();
