"""NEXVATE launch-30 static posts (Instagram + Facebook).

Source plan: ~/Downloads/Nexvate_Social_Brand_System.pdf (30-day launch strategy).
Only the static days live here - Reels (days 2, 12, 18, 26) and Story polls
(days 7, 19) are handled by hand.

Every factual claim is taken from nexvate.ae (services seeder, portfolio) or
from the plan itself. Nothing is invented: no client counts, no years in
business, no made-up statistics.

Slide types:
  cover  kicker, title, sub
  point  n (optional), title, body
  list   title, items
  cta    title, sub, lines (optional)
  single kicker, title, sub, items (optional), foot

Caption placeholders: {CTA} becomes the platform-specific call to action
(cta_ig on Instagram, cta_fb on Facebook, which carries the tracked link).
"""

SITE = "https://nexvate.ae"
WA = "+971 55 167 7805"


def link(path, day):
    return f"{SITE}{path}?utm_source=facebook&utm_medium=social&utm_campaign=launch30&utm_content=d{day:02d}"


POSTS = [
    # ── WEEK 1 ────────────────────────────────────────────────────────────
    dict(
        day=1, pillar="Brand", bg="gradient", path="/",
        slides=[
            dict(t="cover", kicker="Now open · UAE", title="Build.<br>Launch.<br>Grow.",
                 sub="NEXVATE is a UAE digital studio. We build the product — and the pipeline that sells it."),
            dict(t="point", title="Most businesses hire three agencies for one job.",
                 body="One builds the site. One runs the ads. One “does SEO”. And nobody owns the result."),
            dict(t="point", title="We do all three. Under one roof.",
                 body="Apps, websites, stores and automation on one side. SEO, Google Ads and Meta Ads on the other. One team, one plan."),
            dict(t="list", title="How we work",
                 items=["A written scope before we start", "A fixed price, agreed up front",
                        "Code and ad accounts in your name", "Reports on leads, not impressions"]),
            dict(t="cta", title="Follow for one practical tip a week.",
                 sub="Building and growing a business online in the UAE — without the fluff."),
        ],
        caption=(
            "NEXVATE is officially open.\n\n"
            "We're a UAE digital studio that builds the product and the pipeline that sells it — "
            "from a mobile app or Shopify store to the Google and Meta campaigns that fill your calendar.\n\n"
            "Why we exist: most businesses end up hiring three agencies for one job. One builds the site, "
            "one runs the ads, one “does SEO” — and when results don't come, everyone points at someone else.\n\n"
            "We'd rather own the result.\n\n"
            "Swipe to see how we work →\n\n"
            "{CTA}"
        ),
        cta_ig="Follow @nexvate.ae for one practical tip a week on growing your business online in the UAE.",
        cta_fb="Follow the page for one practical tip a week — and see what we do at {LINK}",
        hashtags=["dubai", "uae", "dubaibusiness", "digitalagency", "entrepreneur"],
    ),
    dict(
        day=3, pillar="Brand", bg="powder", path="/services",
        slides=[
            dict(t="cover", kicker="What we do", title="11 services.<br>Two jobs.",
                 sub="We build it. Then we grow it."),
            dict(t="list", title="Build",
                 items=["Mobile App Development", "Custom Web Development", "Shopify Development",
                        "WordPress Development", "AI & Automation", "UI/UX Design",
                        "Website Maintenance & Support"]),
            dict(t="list", title="Grow",
                 items=["SEO Services", "Google Ads Management", "Meta Ads & Social Media",
                        "Consulting & Strategy"]),
            dict(t="point", title="Pick one. Or let them work together.",
                 body="A new store is worth more with ads behind it. Ads are worth more with a site that converts. That's the point of one team."),
            dict(t="cta", title="Not sure where to start?",
                 sub="Send us a DM with the one thing you're trying to fix."),
        ],
        caption=(
            "Everything we do fits into two jobs: build it, then grow it.\n\n"
            "BUILD → mobile apps, custom web development, Shopify, WordPress, AI & automation, UI/UX design, and website maintenance.\n\n"
            "GROW → SEO, Google Ads, Meta Ads & social media, and consulting & strategy.\n\n"
            "You can hire us for one. But they work best together — a new store earns more with ads behind it, "
            "and ads earn more when the site actually converts.\n\n"
            "Save this so you know who to call.\n\n"
            "{CTA}"
        ),
        cta_ig="Not sure where to start? DM us the one thing you're trying to fix.",
        cta_fb="Every service, explained: {LINK}",
        hashtags=["dubai", "uaebusiness", "webdevelopment", "digitalmarketing", "smallbusiness"],
    ),
    dict(
        day=4, pillar="Development", bg="powder", path="/services/mobile-app-development",
        slides=[
            dict(t="single", kicker="Service spotlight · Build", title="Your app.<br>On both stores.",
                 sub="iOS and Android apps for UAE businesses — from the first wireframe to a live listing.",
                 items=["Flutter, React Native or native", "Payments, APIs and backend",
                        "App Store & Google Play submission", "Source code is yours"],
                 foot="Mobile App Development"),
        ],
        caption=(
            "Got an app idea that's been sitting in your notes for a year?\n\n"
            "We build native and cross-platform apps for iOS and Android — for UAE businesses, from the first wireframe "
            "to a live listing on the App Store and Google Play.\n\n"
            "✔ Discovery and technical scoping first\n"
            "✔ Flutter or React Native — native iOS/Android where the app needs it\n"
            "✔ Payments, APIs and backend integration\n"
            "✔ Store submission handled for you\n"
            "✔ Source code and repository access, handed over\n\n"
            "{CTA}"
        ),
        cta_ig="Tell us your app idea in a DM — we'll tell you what it takes to build it.",
        cta_fb="See how we build apps: {LINK}",
        hashtags=["appdevelopment", "mobileapp", "flutter", "dubai", "startup"],
    ),
    dict(
        day=5, pillar="Education", bg="cloud", path="/contact",
        slides=[
            dict(t="cover", kicker="Save this", title="3 signs your website is losing customers",
                 sub="…and the fix for each one."),
            dict(t="point", n="01", title="It's slow on a phone.",
                 body="Most of your visitors are on mobile. If the page takes seconds to show anything, they leave before they see what you sell.<br><br><b>Fix:</b> compress images, cut plugins, test on mobile data."),
            dict(t="point", n="02", title="Contacting you takes effort.",
                 body="No WhatsApp button. A phone number buried in the footer. A form with ten fields.<br><br><b>Fix:</b> one clear action on every page — a tap, not a search."),
            dict(t="point", n="03", title="It doesn't answer their question.",
                 body="Price range, location, timings, delivery. If they have to message to find the basics, many won't.<br><br><b>Fix:</b> put the answers on the page."),
            dict(t="cta", title="Which one is yours?",
                 sub="DM us “CHECK” and we'll tell you."),
        ],
        caption=(
            "Your website might be quietly sending customers to your competitors. Here are 3 signs:\n\n"
            "1️⃣ It's slow on a phone — and that's where most of your visitors are.\n"
            "2️⃣ Contacting you takes effort — no WhatsApp button, a buried number, a ten-field form.\n"
            "3️⃣ It doesn't answer the question they came with — price, location, timings, delivery.\n\n"
            "Every one of these is fixable. Swipe for how →\n\n"
            "Save this and check your own site tonight.\n\n"
            "{CTA}"
        ),
        cta_ig="Not sure which one applies? DM us “CHECK”.",
        cta_fb="Want us to check yours? Get in touch: {LINK}",
        hashtags=["websitedesign", "smallbusiness", "businesstips", "dubai", "uae"],
    ),
    dict(
        day=6, pillar="Marketing", bg="sky", path="/services/seo-services",
        slides=[
            dict(t="single", kicker="Service spotlight · Grow", title="Be the answer when they search.",
                 sub="Technical SEO, content and local search for UAE businesses.",
                 items=["Technical audit + ranked fix list", "Keyword research for the UAE market",
                        "Google Business Profile & local SEO", "Fixes implemented — not just listed"],
                 foot="SEO Services"),
        ],
        caption=(
            "When someone in Dubai searches for what you sell — do they find you, or your competitor?\n\n"
            "Our SEO is the work that makes Google (and the AI tools reading Google) understand exactly what you offer:\n\n"
            "✔ A technical audit with fixes ranked by impact\n"
            "✔ Keyword and search-intent research for the UAE market\n"
            "✔ Local SEO and your Google Business Profile\n"
            "✔ Structured data, validated\n"
            "✔ Monthly reports on what moved — and what didn't\n\n"
            "The difference: we implement the fixes ourselves, because we're also the team that builds websites.\n\n"
            "{CTA}"
        ),
        cta_ig="DM us “SEO” and tell us what you want to rank for.",
        cta_fb="Learn more about our SEO services: {LINK}",
        hashtags=["seo", "digitalmarketing", "googleranking", "dubai", "uaebusiness"],
    ),
    # ── WEEK 2 ────────────────────────────────────────────────────────────
    dict(
        day=8, pillar="Development", bg="powder", path="/services/custom-web-development",
        slides=[
            dict(t="cover", kicker="Service spotlight · Build", title="Software that fits how you work.",
                 sub="Custom web development"),
            dict(t="point", title="When a template stops working",
                 body="Booking rules. Approvals. Branches. Pricing logic. If your team spends the day working around the software, the software is wrong."),
            dict(t="list", title="What we build",
                 items=["Booking & reservation systems", "Customer and partner portals",
                        "Dashboards and internal tools", "Payment, ERP & third-party integrations"]),
            dict(t="list", title="What you get",
                 items=["A written spec and data model", "A staging version to sign off",
                        "Production deployment", "Source code — yours on delivery"]),
            dict(t="cta", title="What's the workaround your team hates most?",
                 sub="Tell us in a DM. We'll tell you if it's worth building."),
        ],
        caption=(
            "Off-the-shelf software is great — until your business stops fitting inside it.\n\n"
            "That's when we come in. We build web applications, portals and internal systems around how your business "
            "actually works, instead of bending your business to fit a template.\n\n"
            "→ Booking and reservation systems\n"
            "→ Customer and partner portals\n"
            "→ Dashboards and internal tools\n"
            "→ Payment, ERP and third-party integrations\n\n"
            "Written scope. Fixed price. Source code is yours on delivery.\n\n"
            "{CTA}"
        ),
        cta_ig="Drop the workaround your team hates most in the comments 👇",
        cta_fb="See how we build custom software: {LINK}",
        hashtags=["webdevelopment", "softwaredevelopment", "laravel", "dubai", "techstartup"],
    ),
    dict(
        day=9, pillar="Credibility", bg="powder", path="/contact",
        slides=[
            dict(t="cover", kicker="How we work", title="How we scope a project in 3 steps",
                 sub="So the price you agree is the price you pay."),
            dict(t="point", n="01", title="Discovery call",
                 body="We talk about the problem, not the feature list. What's broken, who uses it, and what “done” looks like."),
            dict(t="point", n="02", title="Written scope",
                 body="Every screen, integration and deliverable in writing — including what's <b>not</b> included. Nothing is assumed."),
            dict(t="point", n="03", title="Fixed price & plan",
                 body="You approve the scope, we agree a price and a delivery plan. Changes are re-scoped in writing — not argued about later."),
            dict(t="cta", title="Have a project in mind?",
                 sub="Book a discovery call — link in bio."),
        ],
        caption=(
            "Why do so many tech projects go over budget? Usually, nobody wrote down what “done” means.\n\n"
            "Here's how we scope every project:\n\n"
            "1. Discovery call — the problem first, not the feature list.\n"
            "2. Written scope — every screen, integration and deliverable, plus what's NOT included.\n"
            "3. Fixed price and plan — changes are re-scoped in writing, never argued about later.\n\n"
            "Boring? Maybe. But it's why the price you agree is the price you pay.\n\n"
            "{CTA}"
        ),
        cta_ig="Have a project in mind? Book a discovery call — link in bio.",
        cta_fb="Have a project in mind? Book a discovery call: {LINK}",
        hashtags=["projectmanagement", "webdevelopment", "entrepreneur", "smallbusiness", "dubai"],
    ),
    dict(
        day=10, pillar="Marketing", bg="sky", path="/services/meta-ads-social-media-marketing",
        slides=[
            dict(t="single", kicker="Service spotlight · Grow", title="Ads that start conversations.",
                 sub="Facebook & Instagram campaigns for a UAE audience that browses and buys on a phone.",
                 items=["Pixel & Conversions API, set up properly", "Creative produced and tested",
                        "A content calendar you approve", "Monthly cost-per-result report"],
                 foot="Meta Ads & Social Media"),
        ],
        caption=(
            "Likes don't pay rent. Conversations do.\n\n"
            "We run Facebook and Instagram campaigns built around the action that matters — usually a customer messaging you.\n\n"
            "For a UAE luxury car dealer, that meant 109 messaging conversations from AED 584.91 of spend, "
            "at AED 4.68 each (Meta Ads Manager, read 16 Sep 2026).\n\n"
            "What's included:\n"
            "✔ Ad account, pixel and Conversions API — set up properly\n"
            "✔ Creative production and structured testing\n"
            "✔ A monthly content calendar you approve in advance\n"
            "✔ A report on spend and cost per result\n\n"
            "{CTA}"
        ),
        cta_ig="Comment “ADS” and we'll send you how we set these campaigns up.",
        cta_fb="See the full case study and our Meta Ads service: {LINK}",
        hashtags=["metaads", "instagrammarketing", "socialmediamarketing", "digitalmarketing", "dubai"],
    ),
    dict(
        day=11, pillar="Education", bg="cloud", path="/services/google-ads-management",
        slides=[
            dict(t="cover", kicker="Save this", title="Google Ads budget mistakes to avoid",
                 sub="5 ways businesses waste ad spend."),
            dict(t="point", n="01", title="No conversion tracking",
                 body="If Google doesn't know what a lead looks like, it optimises for clicks. Track calls, forms and WhatsApp taps first."),
            dict(t="point", n="02", title="No negative keywords",
                 body="“free”, “jobs”, “course”, “DIY”. Without negatives you pay for searches that were never going to buy."),
            dict(t="point", n="03", title="Broad match on a small budget",
                 body="Broad match needs data to learn. On a small daily budget, start with phrase and exact match."),
            dict(t="point", n="04", title="Every ad goes to the homepage",
                 body="Send each ad group to the page that answers that exact search."),
            dict(t="point", n="05", title="Judging by impressions",
                 body="The number that matters is cost per lead. Everything else is a clue, not a result."),
            dict(t="cta", title="Want a second pair of eyes on your account?",
                 sub="DM us “ADS”."),
        ],
        caption=(
            "Spending on Google Ads but the phone isn't ringing? Check these 5 first:\n\n"
            "1. No conversion tracking — Google optimises for clicks instead of leads.\n"
            "2. No negative keywords — you pay for “free”, “jobs” and “DIY” searches.\n"
            "3. Broad match on a small budget — it needs data you don't have yet.\n"
            "4. Every ad goes to the homepage — send each search to the page that answers it.\n"
            "5. Judging by impressions — cost per lead is the only number that pays.\n\n"
            "Save this before your next budget review.\n\n"
            "{CTA}"
        ),
        cta_ig="Want a second pair of eyes on your account? DM us “ADS”.",
        cta_fb="How we manage Google Ads: {LINK}",
        hashtags=["googleads", "ppc", "digitalmarketing", "marketingtips", "dubaibusiness"],
    ),
    dict(
        day=13, pillar="CTA", bg="gradient", path="/contact",
        slides=[
            dict(t="single", kicker="Free offer", title="A free 15-minute website & growth audit.",
                 sub="We look at your site, your Google presence and your ads — and tell you the three things we'd fix first.",
                 items=["No pitch deck", "No obligation", "Just a straight answer"],
                 foot="DM us “AUDIT”"),
        ],
        caption=(
            "Free for UAE businesses: a 15-minute website & growth audit.\n\n"
            "We'll look at three things:\n"
            "→ Your website (speed, mobile, how easy it is to contact you)\n"
            "→ Your Google presence (search and Google Business Profile)\n"
            "→ Your ads, if you're running any\n\n"
            "Then we tell you the three things we'd fix first. No pitch deck, no obligation.\n\n"
            "{CTA}"
        ),
        cta_ig="DM us “AUDIT” with your website link to book your slot.",
        cta_fb="Book your free audit here: {LINK}",
        hashtags=["dubai", "uae", "websiteaudit", "growthmarketing", "smallbusinessowner"],
    ),
    dict(
        day=14, pillar="Credibility", bg="cloud", path="/services",
        slides=[
            dict(t="cover", kicker="Behind the build", title="The tools & tech we build with",
                 sub="Proven stacks — not experiments on your budget."),
            dict(t="list", title="Apps",
                 items=["Flutter", "React Native", "Swift", "Kotlin", "Firebase"]),
            dict(t="list", title="Web & stores",
                 items=["Laravel & PHP 8", "Livewire & Vue", "Tailwind CSS", "Shopify & Liquid",
                        "WordPress & WooCommerce"]),
            dict(t="list", title="AI & automation",
                 items=["WhatsApp Business API", "OpenAI", "Claude", "n8n", "Make & Zapier"]),
            dict(t="list", title="Design & growth",
                 items=["Figma", "Google Ads & GA4", "Google Tag Manager", "Meta Ads Manager & CAPI",
                        "Search Console & Semrush"]),
            dict(t="cta", title="The stack follows the problem.",
                 sub="Tell us what you're building — we'll tell you what we'd use, and why."),
        ],
        caption=(
            "People ask what we build with. Here's the honest list.\n\n"
            "📱 Apps: Flutter, React Native, Swift, Kotlin, Firebase\n"
            "💻 Web & stores: Laravel, Livewire, Vue, Tailwind, Shopify, WordPress & WooCommerce\n"
            "🤖 AI & automation: WhatsApp Business API, OpenAI, Claude, n8n, Make, Zapier\n"
            "📈 Design & growth: Figma, Google Ads, GA4, Tag Manager, Meta Ads Manager, Search Console, Semrush\n\n"
            "But the stack always follows the problem — not the other way round.\n\n"
            "{CTA}"
        ),
        cta_ig="Building something? Tell us in a DM and we'll tell you what we'd use.",
        cta_fb="See what we build with each stack: {LINK}",
        hashtags=["techstack", "webdevelopment", "flutter", "laravel", "developer"],
    ),
    # ── WEEK 3 ────────────────────────────────────────────────────────────
    dict(
        day=15, pillar="Development", bg="powder", path="/services/wordpress-development",
        slides=[
            dict(t="single", kicker="Service spotlight · Build", title="A WordPress site your team can actually edit.",
                 sub="Fast, secure WordPress & WooCommerce — no developer on standby.",
                 items=["Custom theme or block templates", "WooCommerce stores & checkout",
                        "Speed & Core Web Vitals work", "30 days of post-launch support"],
                 foot="WordPress & WooCommerce"),
        ],
        caption=(
            "Still emailing your developer every time you need to change a price or a photo?\n\n"
            "We build WordPress and WooCommerce sites that load fast, stay secure, and can be edited by your own team.\n\n"
            "✔ Custom theme or a configured set of block templates\n"
            "✔ WooCommerce store builds and checkout work\n"
            "✔ Page speed and Core Web Vitals\n"
            "✔ Security hardening, backups and an update routine\n"
            "✔ Editor training — plus 30 days of post-launch support\n\n"
            "{CTA}"
        ),
        cta_ig="DM us “WP” if your current site is slow or hard to edit.",
        cta_fb="Learn more about our WordPress work: {LINK}",
        hashtags=["wordpress", "woocommerce", "webdesign", "ecommerce", "dubai"],
    ),
    dict(
        day=16, pillar="Education", bg="cloud", path="/services/ai-automation",
        slides=[
            dict(t="cover", kicker="UAE · AI", title="Why UAE businesses are moving to AI automation",
                 sub="It's less about robots. It's about replies."),
            dict(t="point", n="01", title="Customers message first",
                 body="In the UAE, the enquiry starts on WhatsApp. If nobody answers for hours, they message the next business."),
            dict(t="point", n="02", title="The same questions, all day",
                 body="Prices, location, timings, availability. An assistant trained on your own information answers in seconds — at 2 a.m. too."),
            dict(t="point", n="03", title="Humans do the human part",
                 body="Good automation hands over to a person when it should. Nobody gets stuck talking to a bot."),
            dict(t="point", n="04", title="It plugs into what you use",
                 body="CRM, spreadsheets, email, booking systems — every conversation becomes a record, not a lost chat."),
            dict(t="cta", title="What would you automate first?",
                 sub="Tell us in the comments."),
        ],
        caption=(
            "AI automation in the UAE isn't about replacing your team. It's about replying faster than your competitor.\n\n"
            "→ Customers message first — usually on WhatsApp.\n"
            "→ Most of those messages are the same few questions.\n"
            "→ An assistant trained on your own information answers them in seconds, day or night.\n"
            "→ It hands over to a human when it should.\n"
            "→ And it logs everything in the systems you already use.\n\n"
            "The businesses doing this aren't the biggest. They're the ones who reply first.\n\n"
            "{CTA}"
        ),
        cta_ig="What would you automate first? Tell us in the comments 👇",
        cta_fb="See how we build WhatsApp chatbots and AI assistants: {LINK}",
        hashtags=["aiautomation", "chatbot", "whatsappbusiness", "artificialintelligence", "dubai"],
    ),
    dict(
        day=17, pillar="Marketing", bg="sky", path="/services/google-ads-management",
        slides=[
            dict(t="single", kicker="Service spotlight · Grow", title="Paid search, judged on cost per lead.",
                 sub="Search, Shopping & Performance Max — managed for leads, not impressions.",
                 items=["Account audit & restructure", "Conversion tracking that matches real leads",
                        "You own the ad account", "A plain-language monthly report"],
                 foot="Google Ads Management"),
        ],
        caption=(
            "If your Google Ads report leads with impressions, it's hiding something.\n\n"
            "We manage Search, Shopping and Performance Max campaigns against one number: your cost per lead.\n\n"
            "✔ Account audit and restructure\n"
            "✔ Conversion tracking — including offline conversions\n"
            "✔ Keyword, negative keyword and audience management\n"
            "✔ Landing page and ad creative testing\n"
            "✔ You own the account. We run it.\n\n"
            "{CTA}"
        ),
        cta_ig="DM us “ADS” for a second opinion on your account.",
        cta_fb="Learn more about our Google Ads management: {LINK}",
        hashtags=["googleads", "ppc", "searchmarketing", "leadgeneration", "dubai"],
    ),
    dict(
        day=20, pillar="Credibility", bg="powder", path="/portfolio/bayline-garage-management-software",
        slides=[
            dict(t="cover", kicker="What we're building", title="Meet Bayline.",
                 sub="Our own garage management software for UAE workshops."),
            dict(t="point", title="The problem",
                 body="Independent workshops run on a whiteboard, a WhatsApp thread and hand-written job cards. It works — until a customer calls to ask if the car is ready."),
            dict(t="list", title="8 modules. One record.",
                 items=["Job cards", "Bookings", "Customers", "Vehicles", "Quotations", "Invoices",
                        "Parts stock", "Reporting"]),
            dict(t="point", title="7 WhatsApp follow-ups",
                 body="Service reminders, confirmations, car-ready alerts, review requests, payment chases, win-backs and supplier reorders — sent from the workshop's own number."),
            dict(t="cta", title="Run a workshop?",
                 sub="See it live at bayline.nexvate.ae"),
        ],
        caption=(
            "A look at what we're building right now: Bayline 🔧\n\n"
            "It's our own product — garage management software for independent car workshops in the UAE.\n\n"
            "→ 8 modules: job cards, bookings, customers, vehicles, quotations, invoices, parts stock and reporting\n"
            "→ 7 automated WhatsApp follow-ups, sent from the workshop's own number\n"
            "→ Onboarding done for you: data migration and staff training before go-live\n\n"
            "Same team, same stack and same approach you'd get on a custom build for your business.\n\n"
            "{CTA}"
        ),
        cta_ig="Run a workshop? See it live at bayline.nexvate.ae",
        cta_fb="Read how we built it: {LINK}",
        hashtags=["saas", "autorepair", "garage", "softwaredevelopment", "dubai"],
    ),
    dict(
        day=21, pillar="CTA", bg="gradient", path="/services/consulting-strategy",
        slides=[
            dict(t="single", kicker="Consulting & Strategy", title="Not sure what to build, fix or stop?",
                 sub="Book a free discovery call — a senior second opinion on your digital plan.",
                 items=["Platform & vendor selection", "A prioritised roadmap", "A review of your current agency"],
                 foot="Free discovery call"),
        ],
        caption=(
            "Before you spend on a new website, app or ad agency — get a second opinion.\n\n"
            "Our Consulting & Strategy work is a short, finite engagement, not an open-ended retainer:\n\n"
            "✔ Platform, stack and vendor selection\n"
            "✔ A roadmap prioritised by effort and impact\n"
            "✔ A measurement plan naming the numbers that matter\n"
            "✔ An honest review of your current agency or developer\n\n"
            "It starts with a free discovery call.\n\n"
            "{CTA}"
        ),
        cta_ig="Book your free discovery call — link in bio.",
        cta_fb="Book your free discovery call: {LINK}",
        hashtags=["businessstrategy", "digitalstrategy", "consulting", "entrepreneur", "dubai"],
    ),
    # ── WEEK 4 ────────────────────────────────────────────────────────────
    dict(
        day=22, pillar="Development", bg="powder", path="/services/ui-ux-design",
        slides=[
            dict(t="cover", kicker="Service spotlight · Build", title="Design developers can build from.",
                 sub="UI/UX Design"),
            dict(t="point", title="Good design is mostly decisions.",
                 body="What goes on the screen, what doesn't — and what happens when something goes wrong."),
            dict(t="list", title="What's included",
                 items=["User research & journey mapping", "Wireframes & clickable prototypes",
                        "Every state — not just the happy path", "A design system in Figma",
                        "Accessibility review (WCAG 2.2 AA)"]),
            dict(t="point", title="Handoff that doesn't get lost.",
                 body="Specs, tokens and exported assets — so what gets built is what got approved."),
            dict(t="cta", title="Is your app or site hard to use?",
                 sub="DM us a screenshot. We'll tell you why."),
        ],
        caption=(
            "Pretty isn't the goal. Usable is.\n\n"
            "Our UI/UX design covers the whole journey — from research to screens developers can build from directly:\n\n"
            "✔ User research and journey mapping\n"
            "✔ Wireframes and clickable prototypes you can test with real users\n"
            "✔ Every screen state — errors and empty states included\n"
            "✔ A design system in Figma your next developer can use\n"
            "✔ Accessibility review against WCAG 2.2 AA\n\n"
            "{CTA}"
        ),
        cta_ig="Is your app or site hard to use? DM us a screenshot.",
        cta_fb="See our UI/UX design service: {LINK}",
        hashtags=["uiux", "uxdesign", "uidesign", "figma", "dubai"],
    ),
    dict(
        day=23, pillar="Education", bg="cloud", path="/contact",
        slides=[
            dict(t="cover", kicker="Save this", title="5 things to check before your site goes live"),
            dict(t="point", n="01", title="Every form actually arrives",
                 body="Submit each one. Check the inbox, the spam folder and the CRM."),
            dict(t="point", n="02", title="It works on a real phone",
                 body="Not the browser's mobile view — an actual phone, on mobile data."),
            dict(t="point", n="03", title="Tracking is firing",
                 body="GA4, Meta Pixel, Google Ads conversions. Launch without them and your first month of data is gone."),
            dict(t="point", n="04", title="Google can index it",
                 body="No “noindex” left over from staging. Sitemap submitted. Redirects from old URLs in place."),
            dict(t="point", n="05", title="Backups exist — and restore",
                 body="A backup you've never restored is a hope, not a backup."),
            dict(t="cta", title="Launching soon?",
                 sub="Send us the link. We'll run these 5 checks for free."),
        ],
        caption=(
            "The launch-day checklist most businesses skip:\n\n"
            "1. Every form actually arrives — inbox, spam folder and CRM.\n"
            "2. It works on a real phone, on mobile data.\n"
            "3. Tracking is firing — GA4, Meta Pixel, Google Ads.\n"
            "4. Google can index it — no leftover “noindex”, sitemap submitted, old URLs redirected.\n"
            "5. Backups exist, and you've tested a restore.\n\n"
            "Save this for your next launch. 🔖\n\n"
            "{CTA}"
        ),
        cta_ig="Launching soon? DM us the link and we'll run these 5 checks for free.",
        cta_fb="Launching soon? Send us the link and we'll run these checks for free: {LINK}",
        hashtags=["websitelaunch", "webdevelopment", "seo", "smallbusiness", "dubai"],
    ),
    dict(
        day=24, pillar="Marketing", bg="sky", path="/services/website-maintenance-support",
        slides=[
            dict(t="single", kicker="Website Maintenance & Support", title="A named person who answers when it breaks.",
                 sub="Monthly care for the site you already have.",
                 items=["Scheduled updates", "Daily offsite backups — restores tested",
                        "Uptime & security monitoring", "A report you can read in 2 minutes"],
                 foot="Monthly plans"),
        ],
        caption=(
            "Websites don't break at convenient times.\n\n"
            "Our monthly maintenance keeps the site you already have fast, secure and backed up — with a named person who "
            "replies when something goes wrong.\n\n"
            "✔ Core, theme and plugin updates on a schedule\n"
            "✔ Daily offsite backups, with restores actually tested\n"
            "✔ Uptime monitoring and security patching\n"
            "✔ A monthly allowance for small changes\n"
            "✔ A written report you can read in two minutes\n\n"
            "{CTA}"
        ),
        cta_ig="When did your site last get updated? DM us “CARE” if you're not sure.",
        cta_fb="See our maintenance plans: {LINK}",
        hashtags=["websitemaintenance", "wordpress", "webdevelopment", "smallbusiness", "dubai"],
    ),
    dict(
        day=25, pillar="Credibility", bg="powder", path="/contact",
        slides=[
            dict(t="cover", kicker="Is this you?", title="Who we work best with"),
            dict(t="point", n="01", title="UAE businesses with something real to sell",
                 body="A product, a service, a showroom — and customers who already search for it."),
            dict(t="point", n="02", title="Owners who want one accountable team",
                 body="Not three agencies blaming each other for the same result."),
            dict(t="point", n="03", title="People who judge by leads, not likes",
                 body="We report cost per lead and conversations. If vanity metrics are the goal, we're not the right fit."),
            dict(t="point", n="04", title="Teams ready to decide",
                 body="A clear decision-maker and a written scope beat a long committee every time."),
            dict(t="cta", title="Sound like you?",
                 sub="Book a discovery call — link in bio."),
        ],
        caption=(
            "We're not for everyone — and that's on purpose.\n\n"
            "We work best with:\n"
            "✔ UAE businesses with something real to sell\n"
            "✔ Owners who want one accountable team\n"
            "✔ People who judge by leads, not likes\n"
            "✔ Teams ready to make a decision\n\n"
            "If that's you, we should talk.\n\n"
            "{CTA}"
        ),
        cta_ig="Sound like you? Book a discovery call — link in bio.",
        cta_fb="Sound like you? Let's talk: {LINK}",
        hashtags=["dubaibusiness", "uaebusiness", "entrepreneur", "smallbusiness", "dubai"],
    ),
    dict(
        day=27, pillar="Brand", bg="sky", path="/contact",
        slides=[
            dict(t="single", kicker="Now booking", title="November project slots are open.",
                 sub="We plan our work a month ahead. Want to start in November? Now's the time to talk.",
                 items=["Apps & websites", "Shopify & WordPress", "SEO & ads"],
                 foot="Book a call"),
        ],
        caption=(
            "📅 We're now booking November projects.\n\n"
            "We plan work a month ahead so every project starts with a written scope and a team ready to go.\n\n"
            "If you're planning a new website, app, store or ad campaign for November — now's the time to talk.\n\n"
            "{CTA}"
        ),
        cta_ig="DM us “NOVEMBER” or book a call — link in bio.",
        cta_fb="Book a call: {LINK}",
        hashtags=["dubai", "uae", "dubaibusiness", "webdevelopment", "digitalmarketing"],
    ),
    dict(
        day=28, pillar="Education", bg="cloud", path="/services",
        slides=[
            dict(t="cover", kicker="Save this", title="Build vs. buy: choosing the right platform"),
            dict(t="point", title="Buy when…",
                 body="Your process is standard, speed matters, and a monthly fee beats a build cost. Think Shopify, WordPress, SaaS."),
            dict(t="point", title="Build custom when…",
                 body="The software <i>is</i> your advantage, off-the-shelf forces workarounds, or per-seat fees keep climbing."),
            dict(t="list", title="Quick guide",
                 items=["Online store → Shopify", "Content & marketing site → WordPress",
                        "Bookings, portals, workflows → Custom", "Customer app → Flutter / native"]),
            dict(t="point", title="The expensive mistake",
                 body="Building what you could have bought — or bending your business around software that doesn't fit."),
            dict(t="cta", title="Stuck between the two?",
                 sub="DM us. You'll get a straight answer."),
        ],
        caption=(
            "Build or buy? It's the most expensive decision in any digital project.\n\n"
            "BUY (Shopify, WordPress, SaaS) when your process is standard and speed matters.\n"
            "BUILD custom when the software is your advantage — or off-the-shelf keeps forcing workarounds.\n\n"
            "Quick guide:\n"
            "🛒 Online store → Shopify\n"
            "📰 Content & marketing site → WordPress\n"
            "⚙️ Bookings, portals, workflows → Custom build\n"
            "📱 Customer app → Flutter / native\n\n"
            "Save this for your next project. 🔖\n\n"
            "{CTA}"
        ),
        cta_ig="Stuck between the two? DM us — you'll get a straight answer.",
        cta_fb="Stuck between the two? Talk to us: {LINK}",
        hashtags=["shopify", "wordpress", "softwaredevelopment", "startup", "dubai"],
    ),
    dict(
        day=29, pillar="Credibility", bg="powder", path="/",
        slides=[
            dict(t="cover", kicker="30 days in", title="What we've shared this month"),
            dict(t="list", title="Services we spotlighted",
                 items=["Mobile apps", "Custom web", "Shopify & WordPress", "AI & automation",
                        "UI/UX design", "SEO, Google & Meta Ads", "Maintenance"]),
            dict(t="list", title="Guides worth saving",
                 items=["3 signs your site is losing customers", "Google Ads budget mistakes",
                        "5 checks before you launch", "Build vs. buy"]),
            dict(t="point", title="What we're building",
                 body="Bayline — our own garage management software for UAE workshops. Live at bayline.nexvate.ae."),
            dict(t="cta", title="Missed one?",
                 sub="It's all on the grid. Save the ones you need."),
        ],
        caption=(
            "30 days ago we opened NEXVATE. Here's what we've shared since:\n\n"
            "✔ Every service we offer — apps, custom web, Shopify, WordPress, AI, UI/UX, SEO, Google Ads, Meta Ads and maintenance\n"
            "✔ Guides: 3 signs your site is losing customers, Google Ads mistakes, the pre-launch checklist, build vs. buy\n"
            "✔ A look at Bayline, the garage software we're building\n\n"
            "Thank you for following along. This is just the start.\n\n"
            "{CTA}"
        ),
        cta_ig="Which post helped most? Tell us in the comments 👇",
        cta_fb="Thank you for following along. Everything we do: {LINK}",
        hashtags=["dubai", "uae", "digitalagency", "dubaibusiness", "entrepreneur"],
    ),
    dict(
        day=30, pillar="CTA", bg="gradient", path="/contact",
        slides=[
            dict(t="cover", kicker="Let's talk", title="Let's build your next project.",
                 sub="Apps. Websites. Stores. Automation. Ads."),
            dict(t="point", n="01", title="Tell us what you're trying to fix",
                 body="A slow site. A quiet inbox. A manual process. Start with the problem."),
            dict(t="point", n="02", title="Get a written scope",
                 body="What we'll build or run, what's included — and a fixed price."),
            dict(t="point", n="03", title="We build it. Then we grow it.",
                 body="One team from first wireframe to the campaign that fills your calendar."),
            dict(t="cta", title="Book a call",
                 lines=["nexvate.ae/contact", f"WhatsApp {WA}", "info@nexvate.ae"]),
        ],
        caption=(
            "Let's build your next project.\n\n"
            "Here's how it works:\n"
            "1. Tell us what you're trying to fix.\n"
            "2. Get a written scope with a fixed price.\n"
            "3. We build it — then we grow it.\n\n"
            f"📲 WhatsApp: {WA}\n"
            "✉️ info@nexvate.ae\n\n"
            "{CTA}"
        ),
        cta_ig="Or book a call — link in bio.",
        cta_fb="Or book a call: {LINK}",
        hashtags=["dubai", "uae", "dubaibusiness", "webdevelopment", "digitalmarketing"],
    ),
]

# Grid tile headline for each day, word for word from the plan's Instagram grid
# (pages 4-5). Slide 1 of every post is that tile.
TOPICS = {
    1: "Launch post: who Nexvate is & why we exist",
    3: "What we do: full service overview",
    4: "Service spotlight: Mobile App Development",
    5: "3 signs your website is losing customers",
    6: "Service spotlight: SEO for UAE businesses",
    8: "Service spotlight: Custom Web Development",
    9: "How we scope a project in 3 steps",
    10: "Service spotlight: Meta Ads & Social Media",
    11: "Google Ads budget mistakes to avoid",
    13: "Free 15-minute website / growth audit",
    14: "The tools & tech stack we build with",
    15: "Service spotlight: WordPress & WooCommerce",
    16: "Why UAE businesses are moving to AI automation",
    17: "Service spotlight: Google Ads Management",
    20: "Project teaser: what we're building right now",
    21: "Free discovery call: Consulting & Strategy",
    22: "Service spotlight: UI/UX Design",
    23: "5 things to check before your site goes live",
    24: "Service spotlight: Website Maintenance & Support",
    25: "Who we work best with (ideal client profile)",
    27: "Announcement: now booking next month's slots",
    28: "Build vs. buy: choosing the right platform",
    29: "30 days in: recap of what we've shared & built",
    30: "Let's build your next project — book a call",
}
for _p in POSTS:
    _p["topic"] = TOPICS[_p["day"]]

# ── Grid colour pattern ──────────────────────────────────────────────────
# Instagram shows the feed in 3 columns, newest top-left. The Reels sit on the
# grid too; the two Story days (7, 19) don't. Launch day posts 3 at once (days
# 1, 3, 4, the ready designs; the day-2 Reel follows the next day) so the
# profile opens on a full row, then it's 1 a day. Every 3rd post in feed order
# (k = 2, 5, 8 ...) is the centre tile, so each time the grid is a whole
# number of rows (launch day, then every 3rd post) the stripe is dead centre.
# In between it sits one column over.
#
# GRID_MODE "A": light sides, gradient centre (default).
# GRID_MODE "B": gradient sides, light centre.
# Light tiles keep the plan's tone for their pillar; a plan-gradient day that
# lands on a light tile becomes Sky, the plan's CTA tint.
import os as _os

GRID_MODE = _os.environ.get("GRID_MODE", "A").upper()

REELS = {
    2: dict(pillar="Brand", topic="Meet the team behind Nexvate", plan_bg="cloud"),
    12: dict(pillar="Development", topic="Service spotlight: Shopify for UAE e-commerce", plan_bg="powder"),
    18: dict(pillar="Development", topic="Service spotlight: AI & Automation (WhatsApp bots)", plan_bg="powder"),
    26: dict(pillar="Engagement", topic="Day-in-the-life / behind the scenes", plan_bg="cloud"),
}
LAUNCH = [1, 3, 4]   # posted together on launch day, in this order

# Reels need ~2 weeks to shoot and edit, so they come later than in the plan.
# Value = calendar slot after launch day (0 = the day after launch).
# 14 = Sat 10 Oct, 17 = Tue 13 Oct, 20 = Fri 16 Oct, 23 = Mon 19 Oct. Day 30,
# the closing CTA, is still the last post.
REEL_SLOTS = {2: 14, 12: 17, 18: 20, 26: 23}

# One plan day per calendar day after launch: the plan order without the
# Reels, with each Reel dropped into its slot.
SEQUENCE = [d for d in range(1, 31) if d not in LAUNCH and d not in REELS]
for _d, _i in sorted(REEL_SLOTS.items(), key=lambda kv: kv[1]):
    SEQUENCE.insert(_i, _d)

_feed = {p["day"] for p in POSTS} | set(REELS)
FEED_DAYS = LAUNCH + [d for d in SEQUENCE if d in _feed]


def is_centre(day):
    return (FEED_DAYS.index(day) + 1) % 3 == 2


def grid_bg(day, plan_bg, mode=None):
    mode = mode or GRID_MODE
    light = "sky" if plan_bg == "gradient" else plan_bg
    dark_here = is_centre(day) if mode == "A" else not is_centre(day)
    return "gradient" if dark_here else light


for _p in POSTS:
    _p["plan_bg"] = _p["bg"]
    _p["bg"] = grid_bg(_p["day"], _p["plan_bg"])
for _d, _r in REELS.items():
    _r["day"] = _d
    _r["bg"] = grid_bg(_d, _r["plan_bg"])
