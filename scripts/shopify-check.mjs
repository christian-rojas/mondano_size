// Verifica la conexión con la Admin API de Shopify.
// Uso: node --env-file=.env.local scripts/shopify-check.mjs
//
// No imprime secretos: solo la tienda, los scopes y si el catálogo es accesible.

const SHOP = process.env.SHOPIFY_SHOP;
const API = process.env.SHOPIFY_API_VERSION || "2026-10";
const ID = process.env.SHOPIFY_CLIENT_ID;
const SECRET = process.env.SHOPIFY_CLIENT_SECRET;

if (!SHOP || !ID || !SECRET) {
  console.error("Faltan SHOPIFY_SHOP / SHOPIFY_CLIENT_ID / SHOPIFY_CLIENT_SECRET.");
  console.error("Ejecuta: node --env-file=.env.local scripts/shopify-check.mjs");
  process.exit(1);
}

async function token() {
  const res = await fetch(`https://${SHOP}.myshopify.com/admin/oauth/access_token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "client_credentials",
      client_id: ID,
      client_secret: SECRET,
    }),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`token ${res.status}: ${text.slice(0, 200)}`);
  return JSON.parse(text);
}

async function gql(tok, query) {
  const res = await fetch(`https://${SHOP}.myshopify.com/admin/api/${API}/graphql.json`, {
    method: "POST",
    headers: { "X-Shopify-Access-Token": tok, "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`graphql ${res.status}: ${text.slice(0, 200)}`);
  return JSON.parse(text);
}

(async () => {
  console.log(`Tienda: ${SHOP} · API ${API}`);

  const t = await token();
  console.log(`Token: OK · scopes: ${t.scope}`);

  const shop = await gql(t.access_token, "{ shop { name myshopifyDomain currencyCode } }");
  if (shop.errors) throw new Error(JSON.stringify(shop.errors).slice(0, 200));
  const s = shop.data.shop;
  console.log(`Shop: ${s.name} (${s.myshopifyDomain}) · ${s.currencyCode}`);

  const products = await gql(t.access_token, "{ productsCount { count } }");
  if (products.errors) {
    console.log("Catálogo: SIN ACCESO (falta el scope read_products)");
    console.log("  " + JSON.stringify(products.errors[0]?.message || products.errors).slice(0, 120));
  } else {
    console.log(`Catálogo: ${products.data.productsCount.count} productos`);
  }
})().catch((e) => {
  console.error("ERROR:", e.message);
  process.exit(1);
});
